from flask import Flask, request, jsonify
from datetime import datetime
from database import db
from models import Employee, LeaveRequest
from flask import send_from_directory


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leave_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    
    
@app.route('/')
def home():
    return send_from_directory('frontend', 'index.html')

# Add new employee
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json
    try:
        emp = Employee(
            name=data['name'],
            email=data['email'],
            department=data['department'],
            joining_date=datetime.strptime(data['joining_date'], "%Y-%m-%d").date()
        )
        db.session.add(emp)
        db.session.commit()
        return jsonify({"message": "Employee added successfully", "employee_id": emp.id}), 201
    except Exception as e:
        return jsonify({"message": "Employee already exist "}), 400

# Apply for leave
@app.route('/leave/apply', methods=['POST'])
def apply_leave():
    data = request.json
    emp = Employee.query.get(data['employee_id'])
    if not emp:
        return jsonify({"message": "Employee not found"}), 404

    start = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
    end = datetime.strptime(data['end_date'], "%Y-%m-%d").date()

    if start < emp.joining_date:
        return jsonify({"message": "Cannot apply before joining date"}), 400
    if end < start:
        return jsonify({"message": "Invalid date range"}), 400

    days = (end - start).days + 1
    if days > emp.leave_balance:
        return jsonify({"message": "Not enough leave balance"}), 400

    overlap = LeaveRequest.query.filter(
        LeaveRequest.employee_id == emp.id,
        LeaveRequest.start_date <= end,
        LeaveRequest.end_date >= start
    ).first()
    if overlap:
        return jsonify({"message": "Leave overlaps with existing request"}), 400

    leave = LeaveRequest(
        employee_id=emp.id,
        start_date=start,
        end_date=end,
        reason=data.get('reason', '')
    )
    db.session.add(leave)
    db.session.commit()
    return jsonify({"message": "Leave request submitted", "leave_id": leave.id}), 200

# Approve or Reject leave
@app.route('/leave/<int:leave_id>', methods=['PUT'])
def update_leave_status(leave_id):
    data = request.json
    leave = LeaveRequest.query.get(leave_id)
    if not leave:
        return jsonify({"message": "Leave request not found"}), 404
    if leave.status in ["approved", "rejected"]:
        return jsonify({"message": "Leave already processed"}), 400

    leave.status = data['status']
    if leave.status == "approved":
        days = (leave.end_date - leave.start_date).days + 1
        leave.employee.leave_balance -= days
    db.session.commit()
    return jsonify({"message": f"Leave {leave.status}"}), 200

#  leave balance
@app.route('/leave/balance/<int:employee_id>', methods=['GET'])
def get_leave_balance(employee_id):
    emp = Employee.query.get(employee_id)
    if not emp:
        return jsonify({"message": "Employee not found"}), 404
    return jsonify({"employee_id": emp.id, "leave_balance": emp.leave_balance}), 200

#  leave applications with employee details
@app.route('/leave/applications', methods=['GET'])
def get_all_leave_applications():
    leaves = LeaveRequest.query.all()
    result = []
    for leave in leaves:
        result.append({
            "leave_id": leave.id,
            "employee_id": leave.employee.id,
            "employee_name": leave.employee.name,
            "department": leave.employee.department,
            "start_date": leave.start_date.strftime("%Y-%m-%d"),
            "end_date": leave.end_date.strftime("%Y-%m-%d"),
            "reason": leave.reason,
            "status": leave.status
        })
    return jsonify(result), 200

#  applications by status
@app.route('/leave/applications/<status>', methods=['GET'])
def get_leave_applications_by_status(status):
    status = status.lower()
    if status not in ["pending", "approved", "rejected"]:
        return jsonify({"message": "Invalid status"}), 400
    
    leaves = LeaveRequest.query.filter_by(status=status).all()
    result = []
    for leave in leaves:
        result.append({
            "leave_id": leave.id,
            "employee_id": leave.employee.id,
            "employee_name": leave.employee.name,
            "department": leave.employee.department,
            "start_date": leave.start_date.strftime("%Y-%m-%d"),
            "end_date": leave.end_date.strftime("%Y-%m-%d"),
            "reason": leave.reason,
            "status": leave.status
        })
    return jsonify(result), 200



if __name__ == '__main__':
    app.run(debug=True)
