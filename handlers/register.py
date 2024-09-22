from flask import request, jsonify
from flask_restful import Resource
from db.mysqlconn import db

class Register(Resource):
    def post(self):
        print("18")
        req_data = request.get_json()
        print("18")
        result = register(req_data)
        print("18")
        return {"res_status": result['res_status'], "data": result.get('data'), "msg": result.get('msg')}

def register(req_data):
    # db = mydb()
    cursor = db.cursor()
    email = req_data['email'].lower()
    password = req_data['password']
    usertype_id = req_data['usertype_id']

    try:
        print("18")
        query = 'INSERT INTO users (email, password, user_type) VALUES (%s, %s, %s);'
        print("24")
        cursor.execute(query, (email, password, usertype_id))
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
        # db.close()
