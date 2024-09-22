from flask_restful import Resource
from flask import request, jsonify
from db.mysqlconn import db
from flask import jsonify

class StudentData(Resource):
    def post(self):
        try:
            print("7")
            req_data = request.get_json()
            print("9-login-reqdata",req_data)
            app_id = req_data['app_id']
            status_id = req_data['status_id']  
            result = admissions_update(app_id,status_id)
            print("11 result", result)
            if result['res_status']:
                # return {"data": result.get('data'), "msg": "Success"}, 200
                return jsonify({"data": result.get('data'), "msg": "Success"})
            else:
                return {"msg": result.get('msg')}, 500
        except Exception as e:
            # return {"msg": str(e)}, 500
            return jsonify({"msg": str(e)}), 500

def admissions_update(app_id,status_id):
    cursor = db.cursor()

    try:
        print("28")
        query = f'update admissions set status = {status_id} where id = {app_id};'
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
      
