from json import loads
from bson.json_util import dumps
from pymongo import MongoClient
from flask import jsonify
from datetime import datetime

def get_emp_templ_dic():
    templ = dict()
    templ["_id"] = False
    fields = ["depid", "email", "empid", "fullname", "gender", "leave", "phone", "salary", "dob"]

    i = 0
    n_field = len(fields)

    while(i < n_field):
        templ[fields[i]] = True
        i += 1
    return templ

def convert_to_json_object(data):
    return loads(dumps(data))


def send_response(succ=False, mess=None, result=None, typ=None):
    return jsonify(success=succ, message=mess, data=result, type=typ)


class AccountDb:
    def __init__(self, db_uri, db_name):
        self.db = MongoClient(
            db_uri,
            maxPoolSize=50,
            connectTimeoutMS=2500,
        )[db_name]

        # Xem danh sách collection
        # print(self.db.list_collection_names())

        # Lấy collection employee
        self.emps = self.db.employee_info

    # Lấy empid từ emp_email
    def get_empid_by_emp_eml(self, em):
        try:
            pipes = [
                {
                    "$match": {
                        "email": em
                        }
                }, 
                {
                    "$project": {
                        "empid": True, 
                        "_id": False
                        }
                }
            ]
            res = list(self.emps.aggregate(pipes))
            return send_response(True, 'Đã lấy được mã nhân viên theo email', convert_to_json_object(res[0]), 'Ok')
        except Exception as e:
            return send_response(False, e, None, 'Db-error')

    # Lấy thông tin user từ email token

    def get_emp_by_em(self, em):
        try:
            # Ngoại trừ field "_id" ra, các field còn lại nếu muốn không xuất hiện từ không được thêm, thay vì set False -> lỗi
            # pipe tham khảo: https://www.mongodb.com/docs/manual/core/aggregation-pipeline-optimization/
            pipelines = [
               {
                "$match":{
                    "email": em
                    }
                },
               { 
                "$project": get_emp_templ_dic()
                }
            ]

            res = list(self.emps.aggregate(pipelines))

            return send_response(True, 'Đã lấy thông tin người dùng', convert_to_json_object(res[0]), 'Ok')

        except Exception as e:
            return send_response(False, e, None, 'Db-error')

    # Kiểm tra mật khẩu khi khi email đã tồn tại

    def check_pw_existed_by_email(self, em, pw):
        query = {
            "email": em,
            "password": pw,
        }

        if self.emps.count_documents(query) == 1:
            return True
        return False

    def check_emp_existed(self, empEmail):
        query = {'email': empEmail}

        if self.emps.find_one(query) is not None:
            return True
        return False

    def add_emp(self, emp_data):
        # Kiểm tra kiểu
        # print(type(emp_data))

        # Kiểm tra trùng lắp
        if self.check_emp_existed(emp_data['email']):
            return send_response(False, 'Email đã tồn tại', None, 'Duplicated')
        try:
            self.emps.insert_one(emp_data)
            # emp_data tự thêm _id trong mongo vào luôn -> phải remove
            emp_data.pop("_id")
            return send_response(True, 'Thêm nhân viên thành công', emp_data, 'Ok')
        except Exception as e:
            return send_response(False, e, None, 'Db-error')
