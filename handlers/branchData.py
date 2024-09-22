from flask import jsonify
from flask_restful import Resource
from db.mysqlconn import db

class BranchData(Resource):
    def get(self):
        try:
            print("7")
            result = branch_data()
            print("11 result", result)
            if result['res_status']:
                return jsonify({"data": result.get('data'), "msg": "Success"})
            else:
                return jsonify({"msg": result.get('msg')}), 500
        except Exception as e:
            return jsonify({"msg": str(e)}), 500

def branch_data():
    cursor = db.cursor()

    try:
        print("18 branch_data")
        query = 'SELECT id, name, address, city, state, country, telephone, contact_person FROM branches;'
        print("24", query)
        cursor.execute(query)
        print("26 branch_data")
       
        raw_data = cursor.fetchall()
        print("28 raw_data", raw_data)
        data = [{'id': id, 'name': name, 'address': address, 'city': city, 'state': state, 'country': country, 'telephone':telephone,'contact_person':contact_person} for id, name, address, city, state, country,telephone, contact_person in raw_data]
        return {'res_status': True, 'data': data}
    
    except Exception as e:
        db.rollback()  # Rollback the transaction if there's an error
        return {"res_status": False, "msg": str(e)}
    
    finally:
        cursor.close()

