import ast
from copy import deepcopy
from json import dumps
from flask import jsonify
# Thòi gian
from datetime import datetime
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
# Db
from pymongo import MongoClient
import redis


def send_response(succ=False, mess=None, result=None, typ=None):
    return jsonify(success=succ, message=mess, data=result, type=typ)

# Hàm tính thời gian làm việc theo giờ với mỗi lần checkout của nhân viên


def cal_productivity_ot(iso_in_time, iso_out_time):

    delta = relativedelta(
        parse(iso_out_time),
        parse(iso_in_time)
    )

    h = delta.hours
    if h < 8:
        return h, 0

    ot = h - 8 + round(delta.minutes/60, 2)
    return 8, ot

# Mongo


class AttendanceDb:

    def __init__(self, db_uri, db_name):

        self.db = MongoClient(
            db_uri,
            maxPoolSize=50,
            connectTimeoutMS=2500,
        )[db_name]

    def sum_prod_ot_per_day(self, log_lst):
        prod_sum = 0
        ot_sum = 0
        for l in log_lst:
            prod_sum += l["productivity"]
            ot_sum += l["ot"]
        return prod_sum, ot_sum

    # Thống kê check theo ngày tháng và năm
    def get_log_statistic(self, emp_id):
        logs = self.db.get_collection(emp_id)
        now = datetime.now()

        filtr = {
            "year": now.year
        }
        prjtn = {
            "year": False,
            "_id": False,
            "logs.checkin": False,
            "logs.checkout": False
        }

        lg_lst = list(logs.find(filtr, prjtn))
        n_logs = len(lg_lst)

        if n_logs == 0:
            return None

        work_hours = {
            "productivity": 0,
            "overtime": 0
        }

        statistic = {
            "byDate": deepcopy(work_hours),
            "byWeek": deepcopy(work_hours),
            "byMonth": deepcopy(work_hours),
            "byYear": deepcopy(work_hours)
        }

        i = 0

        while i < n_logs:
            day_log = lg_lst[i]

            # Tổng productivity và ot trong ngày
            producties, ots = self.sum_prod_ot_per_day(day_log["logs"])

            # Thống kê theo năm
            statistic["byYear"]["productivity"] += producties
            statistic["byYear"]["overtime"] += ots

            # Thống kê theo tháng
            if day_log["month"] == now.month:

                statistic["byMonth"]["productivity"] += producties
                statistic["byMonth"]["overtime"] += ots

                if day_log["weekday"] <= now.weekday():

                    statistic["byWeek"]["productivity"] += producties
                    statistic["byWeek"]["overtime"] += ots

                    if day_log["day"] == now.day:

                        statistic["byDate"]["productivity"] += producties
                        statistic["byDate"]["overtime"] += ots

            i += 1
        return statistic

    # Tạo document checklog mới

    def create_check_log(self, in_time, out_time):
        now = datetime.now()
        log_filter = {
            "day": now.day,
            "month": now.month,
            "year": now.year
        }

        tm_fm = "%H:%M:%S"
        new_log = {
            "checkin": parse(in_time).strftime(tm_fm),
            "checkout": parse(out_time).strftime(tm_fm),
            "productivity": None,
            "ot": None
        }

        new_log["productivity"], new_log["ot"] = cal_productivity_ot(
            in_time, out_time)

        log_resp = deepcopy(new_log)
        log_resp["workdate"] = now.strftime("%Y-%m-%d")

        return log_filter, new_log, log_resp

    # Thêm check_log cho nhân viên trong ngày
    def add_emp_check_log(self, empid, checkin, checkout):

        # Tạo check log mới
        date_filter, new_check_log, client_resp = self.create_check_log(
            checkin, checkout)
        logs = self.db.get_collection(empid)

        # Nếu đã tồn tại ngày của nhân viên
        if logs.find_one(date_filter) is not None:
            try:
                update_query = {
                    "$push": {
                        "logs": new_check_log
                    }
                }
                logs.update_one(date_filter, update_query)
            except Exception as e:
                # Test
                print(' ', end="\n")

                print(e)
                print(' ', end="\n")

                return send_response(False, "Lỗi trong db", None, 'Db-error')
            return send_response(True, "Đã lưu thời gian checkout", client_resp, 'Ok')

        # Chưa có thì tạo mới
        try:
            # Tạo query insert
            query = deepcopy(date_filter)
            query["weekday"] = datetime.now().weekday()

            query["logs"] = [new_check_log]
            logs.insert_one(query)

        except Exception as e:
            # Test
            print(' ', end="\n")

            print(e)
            print(' ', end="\n")

            return send_response(False, "Lỗi trong db", None, 'Db-error')
        return send_response(True, "Đã lưu thời gian checkout", client_resp, 'Ok')

# Redis


class SnapShotDb:

    def __init__(self, host_name, port_num):
        self.db = redis.Redis(
            host=host_name,
            port=port_num
        )

    # Cập nhật thống kê giờ làm trên redis
    def update_work_statistics(self, emp_id, in_str, out_str):

        prod, ot = cal_productivity_ot(in_str, out_str)
        stats = self.get_work_hour_statistic(emp_id)


        stats["byDate"]["productivity"] += prod
        stats["byDate"]["overtime"] += ot

        stats["byWeek"]["productivity"] += prod
        stats["byWeek"]["overtime"] += ot

        stats["byMonth"]["productivity"] += prod
        stats["byMonth"]["overtime"] += ot

        stats["byYear"]["productivity"] += prod
        stats["byYear"]["overtime"] += ot


        key = emp_id + ":" + "whstats"
        self.db.set(key, dumps(stats))

    # Lấy trạng thái check

    def get_check_status(self, emp_id):
        key = emp_id + ":" + "checkstatus"

        res = self.db.get(key)
        if res == None:

            return send_response(False, 'Nhân viên chưa checkin', None, 'Non-existed')

        if int(res) == 0:
            return send_response(True, 'Nhân viên đang checkout', False, 'Ok')

        return send_response(True, 'Nhân viên đang checkin', True, 'Ok')

    # Đặt trạng thái đăng check
    def set_check_status(self, emp_id):
        key = emp_id + ":" + "checkstatus"

        # Kiểu bool
        stts = self.db.get(key)
        if stts == None:

            self.db.set(key, 0)
            return send_response(False, 'Nhân viên chưa checkin', None, 'Non-existed')

        # Đang checkout
        if int(stts) == 0:
            stts = 1

        else:
            stts = 0

        self.db.set(key, stts)
        return send_response(True, 'Đã cập nhật trạng thái check của nhân viên', None, 'Ok')

    # data có kiểu là dict
    def set_wh_stats(self, emp_id, data):
        key = emp_id + ":" + "whstats"

        self.db.set(key, dumps(data))

    def get_work_hour_statistic(self, emp_id):
        key = emp_id + ":" + "whstats"

        res = self.db.get(key)
        if res is None:
            
            return None
        statistc = ast.literal_eval(res.decode("UTF-8"))

        # Test
        # print(type(statistc))
        return statistc

    def get_check_in(self, emp_id):
        key = emp_id + ":" + "checkin"
        emp_checkin = self.db.get(key)

        self.db.delete(key)

        return emp_checkin

    def set_check_in(self, tim_str, emp_id):
        key = emp_id + ":" + "checkin"
        self.db.set(key, tim_str)
