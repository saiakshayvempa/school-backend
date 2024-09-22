from flask import jsonify
from flask_restful import Resource
from flask import request, jsonify

from db.mysqlconn import db

class StudentGrades(Resource):
    def post(self):
        try:
            print("7")
            req_data = request.get_json()
            print("9-login-reqdata",req_data)
            if req_data['action'] == 'grades':
                result = student_grades(req_data)
            elif req_data['action'] == 'class':
                result = class_grades(req_data)
            elif req_data['action'] == 'all':
                result = all_grades(req_data)
            elif req_data['action'] == 'update':
                result = grades_update(req_data)
            elif req_data['action'] == 'insert':
                result = insert_grades(req_data)
            else:
                result = default_grades(req_data)
           
            print("11 result", result)
            if result['res_status']:
                return jsonify({"data": result.get('data'), "msg": "Success"})
            else:
                return jsonify({"msg": result.get('msg')}), 500
        except Exception as e:
            return jsonify({"msg": str(e)}), 500


def default_grades(req_data):
    cursor = db.cursor()

    try:
        print("28 req_data")
        student_id = req_data['student_id']
   
        query = f'select id,student_id,grade,sub_1,sub_2,sub_3,sub_4,sub_5,sub_6,max_score,max_total,result,exam_type from student_grades where student_id = {student_id} ;'
        print("24 query",query)
        cursor.execute(query,)
        raw_data = cursor.fetchall()
        print("28 raw_data", raw_data)
        data = [{'id': id, 'student_id':student_id,'grade': grade,'sub_1': sub_1,'sub_2': sub_2,'sub_3': sub_3,'sub_4': sub_4,'sub_5': sub_5,'sub_6': sub_6,'max_score':max_score,'max_total':max_total,'result':result, 'exam_type':exam_type} for id,student_id,grade,sub_1,sub_2,sub_3,sub_4,sub_5,sub_6,max_score,max_total,result,exam_type in raw_data]  # Adjusted to include field names # Adjusted to include field names
        return {'res_status': True, 'data': data}
    
    except Exception as e:
        db.rollback()  # Rollback the transaction if there's an error
        return {"res_status": False, "msg": str(e)}
    
    finally:
        cursor.close()
        
def student_grades(req_data):
    cursor = db.cursor()

    try:
        print("28 req_data")
        student_id = req_data['student_id']
        grade = req_data['grade']

        # Correcting the SQL query
        query = '''
        SELECT sg.id, sg.student_id, sg.grade, sg.sub_1, sg.sub_2, sg.sub_3, sg.sub_4, sg.sub_5, sg.sub_6, 
            sg.max_score, sg.max_total, sg.result, sg.exam_type, sd.student_name 
        FROM student_grades AS sg
        INNER JOIN student_data AS sd ON sg.student_id = sd.id 
        WHERE sg.student_id = %s AND sg.grade = %s;
        '''

        print("24 query", query)
        cursor.execute(query, (student_id, grade))  # Use parameterized query to prevent SQL injection
        raw_data = cursor.fetchall()

        print("28 raw_data", raw_data)
        data = [{'id': id, 'student_id':student_id,'grade': grade,'sub_1': sub_1,'sub_2': sub_2,'sub_3': sub_3,'sub_4': sub_4,'sub_5': sub_5,'sub_6': sub_6,'max_score':max_score,'max_total':max_total,'result':result, 'exam_type':exam_type,'student_name':student_name} for id,student_id,grade,sub_1,sub_2,sub_3,sub_4,sub_5,sub_6,max_score,max_total,result,exam_type,student_name in raw_data]  # Adjusted to include field names # Adjusted to include field names
        return {'res_status': True, 'data': data}
    
    except Exception as e:
        db.rollback()  # Rollback the transaction if there's an error
        return {"res_status": False, "msg": str(e)}
    
    finally:
        cursor.close()
        
def class_grades(req_data):
    cursor = db.cursor()

    try:
        print("28 req_data")

        grade = req_data['grade']
        query = '''
        SELECT sg.id, sg.student_id, sg.grade, sg.sub_1, sg.sub_2, sg.sub_3, sg.sub_4, sg.sub_5, sg.sub_6, 
               sg.max_score, sg.max_total, sg.result, sg.exam_type, sd.student_name 
        FROM student_grades AS sg
        INNER JOIN student_data AS sd ON sg.student_id = sd.id 
        WHERE sg.grade = %s;
        '''
        print("24 query", query)
        cursor.execute(query, (grade,))  # Corrected: single parameter should be a tuple
        raw_data = cursor.fetchall()
        print("28 raw_data", raw_data)

        data = [
            {
                'id': id,
                'student_id': student_id,
                'grade': grade,
                'sub_1': sub_1,
                'sub_2': sub_2,
                'sub_3': sub_3,
                'sub_4': sub_4,
                'sub_5': sub_5,
                'sub_6': sub_6,
                'max_score': max_score,
                'max_total': max_total,
                'result': result,
                'exam_type': exam_type,
                'student_name': student_name
            }
            for id, student_id, grade, sub_1, sub_2, sub_3, sub_4, sub_5, sub_6, max_score, max_total, result, exam_type, student_name in raw_data
        ]
        return {'res_status': True, 'data': data}
    
    except Exception as e:
        db.rollback()  # Rollback the transaction if there's an error
        return {"res_status": False, "msg": str(e)}
    
    finally:
        cursor.close()

        
def all_grades(req_data):
    cursor = db.cursor()

    try:
        print("28 req_data")
   
        query = f'select id,student_id,grade,sub_1,sub_2,sub_3,sub_4,sub_5,sub_6,max_score,max_total,result from student_grades ;'
        print("24 query",query)
        cursor.execute(query,)
        raw_data = cursor.fetchall()
        print("28 raw_data", raw_data)
        data = [{'id': id, 'grade': grade,'fee': fee} for id,grade,fee in raw_data]  # Adjusted to include field names
        return {'res_status': True, 'data': data}
    
    except Exception as e:
        db.rollback()  # Rollback the transaction if there's an error
        return {"res_status": False, "msg": str(e)}
    
    finally:
        cursor.close()
        
def grades_update(req_data):
    cursor = db.cursor()

    try:
        print("28")
        id = req_data['id']
        grade = req_data['grade']
        fee= req_data['fee']
        student_id = req_data['student_id']
        grade = req_data['grade']
        sub_1 = req_data['sub_1']
        sub_2 = req_data['sub_2']
        sub_3 = req_data['sub_3']
        sub_4 = req_data['sub_4']
        sub_5 = req_data['sub_5']
        sub_6 = req_data['sub_6']
        query = f'update student_grades set grade = {grade}, sub_1= {sub_1},sub_2= {sub_2},sub_3= {sub_3},sub_4= {sub_4},sub_5= {sub_5},sub_6= {sub_6} where id = {id};'
        print("24")
        cursor.execute(query,)
        print("26")
        db.commit()  # Commit the transaction to save changes
        print("28")
       
        return {'res_status': True, 'msg':'Data Updated Successfully'}
    
    except Exception as e:
        db.rollback()  # Rollback the transaction if there's an error
        return {"res_status": False, "msg": str(e)}
    
    finally:
        cursor.close()

def insert_grades(req_data):
    cursor = db.cursor()

    try:
        student_id = req_data['student_id']
        grade = req_data['grade']
        sub_1 = req_data['sub_1']
        sub_2 = req_data['sub_2']
        sub_3 = req_data['sub_3']
        sub_4 = req_data['sub_4']
        sub_5 = req_data['sub_5']
        sub_6 = req_data['sub_6']
        
        # Use parameterized query to prevent SQL injection
        query = '''
            INSERT INTO student_grades 
            (student_id, grade, sub_1, sub_2, sub_3, sub_4, sub_5, sub_6, max_score, max_total)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 100, 600);
        '''
        
        cursor.execute(query, (student_id, grade, sub_1, sub_2, sub_3, sub_4, sub_5, sub_6))
        
        db.commit()  # Commit the transaction to save changes
        
        # If you want to return the ID of the inserted record
        inserted_id = cursor.lastrowid
        return {'res_status': True, 'data': {'inserted_id': inserted_id}}
    
    except Exception as e:
        db.rollback()  # Rollback the transaction if there's an error
        return {"res_status": False, "msg": str(e)}
    
    finally:
        cursor.close()


def delete_grades(req_data):
    cursor = db.cursor()

    try:
        print("28")
        id = req_data['id']
        query = f'DELETE FROM branches where id = {id};'
        print("24")
        cursor.execute(query,)
        print("26")
        db.commit()  # Commit the transaction to save changes
        print("28")
        # If you want to return the ID of the inserted user
        user_id = cursor.lastrowid
        print("31 user_id",user_id)
        return {'res_status': True, 'data': {'user_id': user_id}}
    
    except Exception as e:
        db.rollback()  # Rollback the transaction if there's an error
        return {"res_status": False, "msg": str(e)}
    
    finally:
        cursor.close()
        



