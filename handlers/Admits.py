from flask import jsonify, request
from flask_restful import Resource
from db.mysqlconn import db

class Admits(Resource):
    def post(self):
        try:
            req_data = request.get_json()
            if req_data.get('action') == 'filter':
                result = filter_data(req_data)
            if req_data.get('action') == 'admit':
                result = generateAdmission(req_data)
            else:
                result = default_data(req_data)
            print("Result:", result)
            if result['res_status']:
                return jsonify({"data": result.get('data'), "msg": "Success"})
            else:
                return jsonify({"msg": result.get('msg')}), 500
        except Exception as e:
            return jsonify({"msg": str(e)}), 500
        
        
def generateAdmission(req_data):
    cursor = db.cursor()
    print("req_data",req_data)
    # Correctly extract data from the request
    name = req_data.get('name')
    father_name = req_data.get('father_name')
    mother_name = req_data.get('mother_name')
    student_email = req_data.get('student_email')
    father_email = req_data.get('father_email')
    mother_email = req_data.get('mother_email')
    father_telephone = req_data.get('father_telephone')
    mother_telephone = req_data.get('mother_telephone')
    application_id = req_data.get('application_id')
    address = req_data.get('address')
    is_active = True

    print("40 req_data",req_data)
    
    # Handle missing required fields
    # if not all([name, father_name, mother_name, student_email, father_email, mother_email, father_telephone, mother_telephone, application_id, address]):
    #     return {'res_status': False, 'msg': 'Missing required fields'}

    try:
        print("47 try")
        # Insert data into student_data table
        query = '''
        INSERT INTO student_data 
        (student_name, father_name, mother_name, student_email, father_email, mother_email, address, mother_telephone, father_telephone, application_id, is_active) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        print("54")
        values = (
            name, father_name, mother_name, student_email, father_email,
            mother_email, address, mother_telephone, father_telephone, application_id, is_active
        )
        # Debug print to check values
        print("Executing query with values:", values)
        cursor.execute(query, values)
        print("60")
        # Get the last inserted student ID
        user_id = cursor.lastrowid
        print("63")
        # Insert into users table for each email
        user_queries = [
            (student_email, '123', 1, user_id),
            (father_email, '123', 3, user_id),
            (mother_email, '123', 3, user_id)
        ]
        print("70")
        for email, password, user_type, student_id in user_queries:
            query = 'INSERT INTO users (email, password, user_type, student_id) VALUES (%s, %s, %s, %s);'
            cursor.execute(query, (email, password, user_type, student_id))
        print("74")
        
        query = f"update admissions set status = 4 where id = {application_id}; "
        cursor.execute(query,)
        print("80")
        # Commit the transaction
        db.commit()

        return {'res_status': True, 'msg': 'User accounts created successfully'}

    except Exception as e:
        db.rollback()  # Rollback in case of error
        return {'res_status': False, 'msg': str(e)}

    finally:
        cursor.close()  # Ensure the cursor is closed





def default_data(req_data):
    cursor = db.cursor()
    try:
        print("Fetching default data")
        query = '''
            SELECT 
                a.id, a.name, a.branch, a.admission_type, at.type, 
                a.mobile, a.dob, a.grade, st.type, a.acadamicYear 
            FROM 
                admissions a 
            LEFT JOIN 
                admission_types at ON at.id = a.admission_type 
            LEFT JOIN 
                status_types st ON st.id = a.status 
            WHERE 
                a.status = %s;
        '''
        cursor.execute(query, (2,))
        raw_data = cursor.fetchall()
        print("Raw data fetched:", raw_data)
        data = [{'id': id, 'name': name, 'branch': branch, 'admission_type': admission_type,
                 'admission_type_name': admission_type_name, 'mobile': mobile, 'dob': dob,
                 'grade': grade, 'status': status, 'acadamicYear': acadamicYear}
                for id, name, branch, admission_type, admission_type_name, mobile, dob, grade, status, acadamicYear in raw_data]
        return {'res_status': True, 'data': data}
    
    except Exception as e:
        db.rollback()  # Rollback the transaction if there's an error
        return {"res_status": False, "msg": str(e)}
    
    finally:
        cursor.close()

def filter_data(req_data):
    cursor = db.cursor()
    try:
        where = dynamic_where(req_data)
        query = '''
                    SELECT 
                        a.id, a.name, a.branch, a.admission_type, at.type, 
                        a.mobile, a.dob, a.grade, st.type, a.acadamicYear 
                    FROM 
                        admissions a 
                    LEFT JOIN 
                        admission_types at ON at.id = a.admission_type 
                    LEFT JOIN 
                        status_types st ON st.id = a.status 
                    
                '''
        query = query+" " + where +";"
        print("71 query",query)
        cursor.execute(query)
        raw_data = cursor.fetchall()
        print("Raw data fetched:", raw_data)
        data = [{'id': id, 'name': name, 'branch': branch, 'admission_type': admission_type,
                    'admission_type_name': admission_type_name, 'mobile': mobile, 'dob': dob,
                    'grade': grade, 'status': status, 'acadamicYear': acadamicYear}
                for id, name, branch, admission_type, admission_type_name, mobile, dob, grade, status, acadamicYear in raw_data]
        return {'res_status': True, 'data': data}
    except Exception as e:
        db.rollback()  # Rollback the transaction if there's an error
        return {"res_status": False, "msg": str(e)}

def dynamic_where(req_data):
    where_clauses = []
    
    # Handle 'id' filter
    id_value = req_data.get("id")
    print("88 id_value",id_value)
    
    if id_value is not None:
        where_clauses.append(f"a.id = {id_value}")
    
    # Handle 'grade' filter
    grade_value = req_data.get("grade")
    print("96 grade_value",type(grade_value))
    if grade_value is not "":
        where_clauses.append(f"a.grade = {grade_value}")
    
    # Handle 'name' filter with LIKE operator
    name_value = req_data.get("name")
    if name_value is not "":
        where_clauses.append(f"a.name LIKE '%{name_value}%'")
    print("104 where_clauses",where_clauses)
    # Combine all conditions
    if where_clauses:
        where_clause = "WHERE " + " AND ".join(where_clauses)
    else:
        where_clause = ""  # No conditions
    
    return where_clause

    
