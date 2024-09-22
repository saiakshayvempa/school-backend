from flask import request, jsonify
from flask_restful import Resource
from db.mysqlconn import db
from datetime import datetime

class Admissions(Resource):
    def post(self):
        print("7")
        req_data = request.get_json()
        print("9 req_data", req_data)
        result = admissions(req_data)
        print("11 result", result)
        return {"res_status": result['res_status'], "data": result.get('data'), "msg": result.get('msg')}

def admissions(req_data):
    cursor = db.cursor()
    name = req_data['name']
    branch = req_data['branch']
    admissions_type = req_data['admissionType']
    mobile = req_data['mobile']
    # Convert dob to datetime format
    dob = req_data['dob']
    print("23 dob", dob)
    print("24 dob type", type(dob))
    try:
        # dob = datetime.strptime(dob, '%d-%m-%Y')  # Change format if needed
        dob = datetime.strptime(dob, '%Y-%m-%d')  # Change format if needed
    except ValueError as e:
        return {"res_status": False, "msg": f"Invalid date format for dob: {str(e)}"}

    grade = req_data['grade']
    if grade=="LKG":
        Grade=-2
    elif grade=="UKG":
        Grade=-1
    else:
        Grade=grade
    status = req_data['status']
    academic_year = req_data.get('acadamicYear', "")  # Use get to avoid KeyError

    if academic_year == "":
        academic_year = get_academic_year()

    try:
        print("18")
        query = '''INSERT INTO admissions 
                   (name, branch, admission_type, mobile, dob, grade, status, acadamicYear) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'''  # Corrected placeholders
        print("24")
        cursor.execute(query, (name, branch, admissions_type, mobile, dob, Grade, status, academic_year))
        print("26")
        db.commit()  # Commit the transaction to save changes
        print("28")
        user_id = cursor.lastrowid
        print("31 user_id", user_id)
        return {'res_status': True, 'data': {'user_id': user_id}}
    
    except Exception as e:
        db.rollback()  # Rollback the transaction if there's an error
        return {"res_status": False, "msg": str(e)}
    
    finally:
        cursor.close()
        # db.close()

def get_academic_year():
    # Get the current date
    now = datetime.now()
    
    # Get the current year and month
    current_year = now.year
    current_month = now.month
    
    # Determine the academic year based on the month
    if current_month < 6:  # Before June
        return current_year
    else:  # June or later
        return current_year + 1
