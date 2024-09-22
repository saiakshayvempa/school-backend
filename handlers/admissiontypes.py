from flask_restful import Resource
from db.mysqlconn import db
from flask import jsonify

class AdmissionsTypes(Resource):
    def get(self):
        try:
            print("7")
            result = admissionsTypes()
            print("11 result", result)
            if result['res_status']:
                # return {"data": result.get('data'), "msg": "Success"}, 200
                return jsonify({"data": result.get('data'), "msg": "Success"})
            else:
                return {"msg": result.get('msg')}, 500
        except Exception as e:
            # return {"msg": str(e)}, 500
            return jsonify({"msg": str(e)}), 500

def admissionsTypes():
    cursor = db.cursor()

    try:
        print("18")
        query = 'select id, type from admission_types;'
        print("24", query)
        cursor.execute(query)
        print("26")
       
        raw_data = cursor.fetchall()
        print("28 raw_data", raw_data)
        data = [{'id': id, 'type': name} for id, name in raw_data]  # Adjusted to include field names
        return {'res_status': True, 'data': data}
    
    except Exception as e:
        db.rollback()  # Rollback the transaction if there's an error
        return {"res_status": False, "msg": str(e)}
    
    finally:
        cursor.close()
      
