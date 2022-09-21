# Database
import attendance_db

# Hỗ trợ lấy request
from json import loads
import requests

# Bảo mật với jwt
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required

# Flask
from os import path
from configparser import ConfigParser
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)

# Config
config = ConfigParser()
config.read(path.abspath(path.join(".ini")))

env = 'DEV'
configs = ['DEBUG', 'SERVER_NAME',
           'SERVICE_DB_URI', 'SERVICE_NS',
           'SECRET_KEY', 'JWT_TOKEN_LOCATION',
           'JWT_SECRET_KEY']
i = 0
n_config = len(configs)
while i < n_config:
    conf = configs[i]
    app.config[conf] = config[env][conf]
    i += 1
jwt = JWTManager(app)
CORS(app)

# Db
mongo_db = attendance_db.AttendanceDb(
    config[env][configs[2]],
    config[env][configs[3]]
)
redis_db = attendance_db.SnapShotDb(
    config[env]['REDIS_HOST_NAME'],
    config[env]['REDIS_POST']
)



# Gọi sang account để lấy id từ email tương ứng


def get_empid_by_email(em):
    # Gọi api sử dụng request
    service_url = config[env]['ACCOUNT_SERVICE']
    resp = requests.get(service_url + "/empid", {'email': em})

    return loads(resp.text)['data']['empid']

@app.route('/checkstatus', methods=['POST'])
@jwt_required()
def set_emp_check_status():

    # Lấy mã nhân viên
    emp_em = get_jwt_identity()
    emp_i = get_empid_by_email(emp_em)

    return redis_db.set_check_status(emp_i)

@app.route('/checkstatus', methods=['GET'])
@jwt_required()
def get_emp_check_status():

    # Lấy mã nhân viên
    emp_em = get_jwt_identity()
    emp_i = get_empid_by_email(emp_em)

    #Kiểu bool
    return redis_db.get_check_status(emp_i)



@app.route('/attstatus', methods=['GET'])
@jwt_required()
def get_cur_att_status():
    # Lấy mã nhân viên
    emp_em = get_jwt_identity()
    emp_i = get_empid_by_email(emp_em)

    stats = redis_db.get_work_hour_statistic(emp_i)

    # Nếu redis chưa có thống kê
    if stats is None:
        stats = mongo_db.get_log_statistic(emp_i)

        if stats is None:
            return attendance_db.send_response(False, "Nhân viên chưa đi làm trong khoảng thời gian này", stats, 'Non-existed')

        redis_db.set_wh_stats(emp_i, stats)
        return attendance_db.send_response(True, "Đã lấy thống kê giờ làm của nhân viên", stats, 'Ok')

    return attendance_db.send_response(True, "Đã lấy thống kê giờ làm của nhân viên", stats, 'Ok')


@app.route('/checkin', methods=['POST'])
@jwt_required()
def checkin():
    # Lấy mã nhân viên
    emp_em = get_jwt_identity()
    emp_i = get_empid_by_email(emp_em)

    # Thêm thời gian checkin vào redis
    checkin_time_str = request.get_json()['checktime']
    redis_db.set_check_in(checkin_time_str, emp_i)

    return attendance_db.send_response(True, "Đã lưu thời gian checkin", None, 'Ok')


@app.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    # Lấy mã nhân viên
    emp_em = get_jwt_identity()
    emp_i = get_empid_by_email(emp_em)

    # Lấy thời gian checkin/out
    checkout_time_str = request.get_json()['checktime']
    checkin_time_str = redis_db.get_check_in(emp_i)

    #Cập nhật thống kê trên redis
    redis_db.update_work_statistics(emp_i, checkin_time_str, checkout_time_str)

    # Lưu lịch sử vào mongodb
    return mongo_db.add_emp_check_log(emp_i, checkin_time_str, checkout_time_str)


if __name__ == '__main__':
    app.run()
