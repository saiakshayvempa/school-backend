from flask_restful import Resource
from db.mysqlconn import db
from flask import jsonify

class ApplicationData(Resource):
    def get(self):
        try:
            print("7")
            result = admissions_data()
            print("11 result", result)
            if result['res_status']:
                # return {"data": result.get('data'), "msg": "Success"}, 200
                return jsonify({"data": result.get('data'), "msg": "Success"})
            else:
                return {"msg": result.get('msg')}, 500
        except Exception as e:
            # return {"msg": str(e)}, 500
            return jsonify({"msg": str(e)}), 500

def admissions_data():
    cursor = db.cursor()

    try:
        print("18")
        query = 'select a.id, a.name,a.branch,a.admission_type,at.type,a.mobile,a.dob,a.grade,st.type, a.acadamicYear from admissions a left join admission_types at on at.id = a.admission_type left join status_types st on st.id = a.status;'
        print("24", query)
        cursor.execute(query)
        print("26")
       
        raw_data = cursor.fetchall()
        print("28 raw_data", raw_data)
        data = [{'id': id, 'name': name, 'branch':branch,"admission_type":admission_type,"type":type,"mobile":mobile,"dob":dob,"grade":grade,"status":status,"acadamicYear":acadamicYear} for id, name,branch,admission_type,type,mobile,dob,grade,status,acadamicYear in raw_data]  # Adjusted to include field names
        print("33 data", data)
        return {'res_status': True, 'data': data}
    
    except Exception as e:
        db.rollback()  # Rollback the transaction if there's an error
        return {"res_status": False, "msg": str(e)}
    
    finally:
        cursor.close()
      
