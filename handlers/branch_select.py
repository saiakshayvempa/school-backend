from flask import jsonify, make_response
from flask_restful import Resource
from db.mysqlconn import db

class Branchs(Resource):
    def get(self):
        try:
            result = BranchList()
            if result['res_status']:
                return make_response(jsonify({"data": result.get('data'), "msg": "Success"}), 200)
            else:
                return make_response(jsonify({"msg": result.get('msg')}), 500)
        except Exception as e:
            print("BranchList error", e)
            return make_response(jsonify({"msg": str(e)}), 500)

def BranchList():
    cursor = db.cursor()
    print("18 BranchList")
    try:
        print("21 BranchList")
        query = 'SELECT id, city FROM branches;'
        cursor.execute(query)
        print("24 BranchList")
        raw_data = cursor.fetchall()
        print("24 BranchList raw_data", raw_data)
        # Corrected the variable name and dictionary creation
        data = [{'id': id, 'city': city} for id, city in raw_data]
        print("branch select data 26", data)
        return {'res_status': True, 'data': data}
    
    except Exception as e:
        db.rollback()  # Rollback the transaction if there's an error
        return {"res_status": False, "msg": str(e)}
    
    finally:
        cursor.close()
 
