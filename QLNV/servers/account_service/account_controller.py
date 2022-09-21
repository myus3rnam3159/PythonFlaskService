from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
import account_db
from os import path
from configparser import ConfigParser
from flask import Flask, request
# Dự phòng trường hợp cần đến cors
from flask_cors import CORS


# Tạo đối tượng app
app = Flask(__name__)


# Đọc file ini để lấy config
config = ConfigParser()
config.read(path.abspath(path.join(".ini")))

env = 'DEV'
configs = ['DEBUG', 'SERVER_NAME',
           'SERVICE_DB_URI', 'SERVICE_NS',
           'SECRET_KEY', 'JWT_TOKEN_LOCATION',
            'JWT_SECRET_KEY']



# Tạo đối tượng mongodb client
db = account_db.AccountDb(

    config[env][configs[2]],
    config[env][configs[3]]
)

# Thêm config vào app
i = 0
n_config = len(configs)
while i < n_config:
    conf = configs[i]
    app.config[conf] = config[env][conf]
    i += 1


#Set jwt manager cho app sau khi config
jwt = JWTManager(app)

# Trường hợp cần đến cors
CORS(app)

@app.route('/empid', methods = ['GET'])
def get_empid_by_em():
    em = request.args.get("email")
    if db.check_emp_existed(em) == False:
        return account_db.send_response(False, 'Email không tồn tại', None, 'Non-existed')
    return db.get_empid_by_emp_eml(em)

@app.route('/user', methods=['GET'])
@jwt_required()
def login_by_email_auth():
    emp_eml = get_jwt_identity()
    
    #Test
    #print(emp_eml)

    if db.check_emp_existed(emp_eml) == False:
        return account_db.send_response(False, 'Email không tồn tại', None, 'Non-existed')
    
    return db.get_emp_by_em(emp_eml)


@app.route('/login', methods=['POST'])
def log_emp_in():
    #Test - Kiểu dict
    #print(type(request.get_json()))

    emp_em = request.get_json()['email']
    emp_pw = request.get_json()['password']

    
    # Kiểm tra email tồn tại 
    if db.check_emp_existed(emp_em) == False:
        return account_db.send_response(False, 'Email không tồn tại', None, 'Non-existed')
    
    # Kiểm tra mật khẩu
    if db.check_pw_existed_by_email(emp_em, emp_pw) == False:
        return account_db.send_response(False, 'Mật khẩu không đúng', None, 'Incorrect')
    
    #Tạo token đăng nhập
    access_token = create_access_token(identity = emp_em)
    
    return account_db.send_response(True, 'Đăng nhập thành công', access_token, 'Ok')


@app.route('/register', methods=['POST'])
def create_emp():
    # Vì request gửi data có content-type header = application/json nên được phép dùng request.get_json()
    return db.add_emp(request.get_json())


@app.route('/')
def test():
    return 'Hi'


if __name__ == '__main__':
    app.run()
