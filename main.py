from flask import Flask
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Apply CORS to all routes
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# CORS(app, resources={r"/api/*": {"origins": "*", "allow_headers": "Content-Type"}})

app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

# Your existing code...

# Add resource endpoints
from handlers.login import Login
api.add_resource(Login, '/login')

from handlers.register import Register
api.add_resource(Register, '/register')

# Add Admissions endpoints
from handlers.admissiontypes import AdmissionsTypes
api.add_resource(AdmissionsTypes, '/admissionTypes')

from handlers.admissions import Admissions
api.add_resource(Admissions, '/Admissions')

from handlers.applicationData import ApplicationData
api.add_resource(ApplicationData, '/ApplicationData')

from handlers.applicationUpdate import ApplicationUpdate
api.add_resource(ApplicationUpdate, '/ApplicationUpdate')

from handlers.Admits import Admits
api.add_resource(Admits, '/Admits')

# Branches

from handlers.branch_select import Branchs
api.add_resource(Branchs, '/Branchs')

from handlers.branchData import BranchData
api.add_resource(BranchData, '/BranchData')

# Fees
from handlers.fee_structure import Feestructure
api.add_resource(Feestructure, '/Feestructure')

from handlers.fee_data import FeeData
api.add_resource(FeeData, '/FeeData')

# Students Data
from handlers.student_grades import StudentGrades
api.add_resource(StudentGrades, '/StudentGrades')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
