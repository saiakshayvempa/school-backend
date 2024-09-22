from flask import jsonify
from flask_restful import Resource
from flask import request, jsonify

from db.mysqlconn import db

class Feestructure(Resource):
    def post(self):
        try:
            print("7")
            req_data = request.get_json()
            print("9-login-reqdata",req_data)
            if req_data['action'] == 'update':
                result = fee_update(req_data)
            elif req_data['action'] == 'show':
                result = fee_show(req_data)
            # elif req_data['action'] == 'insert':
            #     result = branch_insert(req_data) 
            # elif req_data['action'] == 'delete':
            #     result = branch_delete(req_data)
            # result = branch_data()
            print("11 result", result)
            if result['res_status']:
                return jsonify({"data": result.get('data'), "msg": "Success"})
            else:
                return jsonify({"msg": result.get('msg')}), 500
        except Exception as e:
            return jsonify({"msg": str(e)}), 500

def fee_show(req_data):
    cursor = db.cursor()

    try:
        print("28 fee_show")
   
        query = f'select id,grade,fee from fee_info;'
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

def branch_delete(req_data):
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




# def branch_insert(req_data):
#     cursor = db.cursor()

#     try:
#         print("28")
#         name = req_data['name']
#         address= req_data['name']
#         city= req_data['name']
#         state= req_data['name']
#         country= req_data['name']
#         telephone= req_data['name']
#         contact_person = req_data['name']
#         query = f"insert into branches (name, address, city, state, country, telephone, contact_person) 
#         values ('{name}','{address}','{city}','{state}','{country}',{telephone}, {contact_person});"
#         print("24")
#         cursor.execute(query,query)
#         print("26")
#         db.commit()  # Commit the transaction to save changes
#         print("28")
#         # If you want to return the ID of the inserted user
#         branch_id = cursor.lastrowid
#         print("96 branch_id",branch_id)
#         return {'res_status': True, 'data': {'branch_id': branch_id}}
    
#     except Exception as e:
#         db.rollback()  # Rollback the transaction if there's an error
#         return {"res_status": False, "msg": str(e)}
    
#     finally:
#         cursor.close()

