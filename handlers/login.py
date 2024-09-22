from flask import request, jsonify
from flask_restful import Resource
from db.mysqlconn import db
import hashlib  # Assuming passwords are hashed

class Login(Resource):
    def post(self):
        req_data = request.get_json()
        print("Login request data received:", req_data)  # For debugging; consider removing in production
        email = req_data['email'].lower()
        password = req_data['password']

        # Hash the password if it's stored as a hash in the database
        # hashed_password = hashlib.sha256(password.encode()).hexdigest()

        result = login(email, password)
        print("17 result",result)
        if result['res_status']:
            if result['user']:
                # return jsonify({"res_status": True, "user": result['user']})
                return {"res_status": True, "user": result['user']}
            else:
                return jsonify({"res_status": False, "msg": "Invalid email or password"})
        else:
            return jsonify(result)

def login(email, hashed_password):
    cursor = db.cursor()
    try:
        query = 'SELECT id, email, user_type, student_id FROM users WHERE email=%s AND password=%s'
        cursor.execute(query, (email, hashed_password))
        user_tuple = cursor.fetchone()
        print("User data fetched:", user_tuple)

        if user_tuple:
            user_dict = {
                'id': user_tuple[0],
                'email': user_tuple[1],
                'user_type_id': user_tuple[2],
                'student_id': user_tuple[3],
            }
            print("user_dict:", user_dict)
            return {'res_status': True, 'user': user_dict}
        else:
            return {'res_status': False, 'msg': 'Invalid email or password'}
    except Exception as e:
        # Log the exception properly here
        return {"res_status": False, "msg": str(e)}
    finally:
        cursor.close()
        # If not using a connection pool, consider closing the db connection here
