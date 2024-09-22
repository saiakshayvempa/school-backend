from flask import jsonify, make_response
from flask_restful import Resource
from flask import request, jsonify
from datetime import datetime

from db.mysqlconn import db



class FeeData(Resource):
    def post(self):
        try:
            req_data = request.get_json()
            
            if req_data['action'] == 'update':
                result = fee_update(req_data)
            elif req_data['action'] == 'info':
                result = student_info(req_data)
            elif req_data['action'] == 'show':
                result = fee_show(req_data)
            elif req_data['action'] == 'current':
                result = fee_data(req_data)

            if result['res_status']:
                return jsonify({"data": result.get('data'), "msg": "Success"})
            else:
                return make_response(jsonify({"msg": result.get('msg')}), 500)
                
        except Exception as e:
            return make_response(jsonify({"msg": str(e)}), 500)



        
def fee_show(req_data):
    cursor = db.cursor()

    try:
        print("28 fee_show")
        student_id = req_data['student_id']
        query = f'select id,student_id,grade,fee,paid,balance,acadamic_year from fee_data where student_id={student_id};'
        print("24 query",query)
        cursor.execute(query,)
        raw_data = cursor.fetchall()
        print("28 raw_data", raw_data)
        data = [{'id': id, 'student_id':student_id,'grade': grade,'fee': fee,"paid":paid,"balance":balance,'acadamic_year':acadamic_year} for id,student_id,grade,fee,paid,balance,acadamic_year in raw_data]  # Adjusted to include field names
        return {'res_status': True, 'data': data}
    
    except Exception as e:
        db.rollback()  # Rollback the transaction if there's an error
        return {"res_status": False, "msg": str(e)}
    
    finally:
        cursor.close()
        
def student_info(req_data):
    cursor = db.cursor()

    try:
        print("28 student_info")
        student_id = req_data['student_id']
        query = f'select id,student_name,father_name,mother_name,address from student_data where id = {student_id};'
        print("24 query",query)
        cursor.execute(query,)
        raw_data = cursor.fetchall()
        print("28 raw_data", raw_data)
        data = [{'id': id, 'student_name': student_name,'father_name': father_name,'mother_name':mother_name,'address':address} for id,student_name,father_name,mother_name,address in raw_data]  # Adjusted to include field names
        return {'res_status': True, 'data': data[0]}
    
    except Exception as e:
        db.rollback()  # Rollback the transaction if there's an error
        return {"res_status": False, "msg": str(e)}
    
    finally:
        cursor.close()
        
def fee_update(req_data):
    cursor = db.cursor()

    try:
        print("28")
        id = req_data['id']
        grade = req_data['grade']
        fee= req_data['fee']
       
        query = f'update fee_info set grade = {grade}, fee= {fee} where id = {id};'
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

def fee_data(req_data):
    cursor = db.cursor()

    try:
        print("28 fee_data")
        student_id = req_data['student_id']
        acadamic_year= get_academic_year()
        acadamic_year = str(acadamic_year)
        query = f'select id,student_id,grade,fee,paid,balance,acadamic_year from  fee_data where student_id = {student_id} and acadamic_year={acadamic_year};'
        print("24 query",query)
        cursor.execute(query,)
        print("26")
        raw_fee = cursor.fetchall()
        print("28 raw_data", raw_fee)
        if len(raw_fee)==0:
            query = f'select current_grade from  student_data where id = {student_id} ;'
            cursor.execute(query,)
            print("26")
            raw_data = cursor.fetchall()
            print("123 raw_data", raw_data)
            grade = raw_data[0][0]
            query =f"select fee from fee_info where grade={grade}"
            cursor.execute(query,)
            raw_data = cursor.fetchall()
            print("128 raw_data", raw_data)
            amount =raw_data[0][0]
            query = f"INSERT INTO fee_data (student_id,grade,fee,paid,balance,acadamic_year) VALUES ({student_id},{grade},{amount},{0},{amount},{acadamic_year} );"
            cursor.execute(query,)
            db.commit()  # Commit the transaction to save changes
            print("28")
            query = f'select id,student_id,grade,fee,paid,balance,acadamic_year from  fee_data where student_id = {student_id} and acadamic_year={acadamic_year};'
            print("24 query",query)
            cursor.execute(query,)
            print("137 inserted")
            raw_fee = cursor.fetchall()
            fee_data =[{'id': id, 'student_id':student_id,'grade': grade,'fee': fee,'paid':paid,'balance':balance,'acadamic_year':acadamic_year} for id,student_id,grade,fee,paid,balance,acadamic_year in raw_fee]
            return {'res_status': True, 'data': fee_data[0]}
        else:
            print(" 142 -->  > ëlse")
            fee_data =[{'id': id, 'student_id':student_id,'grade': grade,'fee': fee,'paid':paid,'balance':balance,'acadamic_year':acadamic_year} for id,student_id,grade,fee,paid,balance,acadamic_year in raw_fee]
            return {'res_status': True, 'data': fee_data[0]}
    
    except Exception as e:
        db.rollback()  # Rollback the transaction if there's an error
        return {"res_status": False, "msg": str(e)}
    
    finally:
        cursor.close()

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
        return current_year 

