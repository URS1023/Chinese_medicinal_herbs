from flask import Flask, request, jsonify
from flask_apscheduler import APScheduler
import datetime
from HuaWei_iot import re_data
import pymysql
import hashlib
import json
import random
import data_analyze as t3
class Config:
    SCHEDULER_API_ENABLED = True  # 允许通过URL访问调度任务接口
    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 2
    }
    SCHEDULER_TIMEZONE = 'UTC'

app = Flask(__name__)
app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# MySQL数据库配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'db': 'flask_user_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

# 加密密码
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 检查用户是否存在
def user_exists(username):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE username = %s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            return result is not None
    finally:
        connection.close()


# 注册用户
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': '2'}), 400  # 请输入账号密码

    if user_exists(username):
        return jsonify({'message': '3'}), 400  # 用户已存在

    hashed_password = hash_password(password)

    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(sql, (username, hashed_password))
        connection.commit()
        return jsonify({'message': '1'}), 201  # 用户注册成功
    except Exception as e:
        connection.rollback()
        return jsonify({'message': str(e)}), 500
    finally:
        connection.close()


# 用户登录
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': '2'}), 400

    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE username = %s"
            cursor.execute(sql, (username,))
            user = cursor.fetchone()

            if user and hash_password(password) == user['password']:
                return jsonify({'message': '1', 'user': user}), 200
            else:
                return jsonify({'message': '0'}), 401
    finally:
        connection.close()


# 定义要定期执行的任务
def save_data():
    connection = pymysql.connect(**db_config)
    try:
        led, temp, humi, sound, tilt, vibrate, fire, smoke, light_sense, event_time = re_data()
        # OFF 81 0 0 0 0 0 156 116 20241207T171738Z
        format_string = "%Y%m%dT%H%M%SZ"
        datetime_object = datetime.datetime.strptime(event_time, format_string)
        event_time = int(datetime_object.timestamp())
        print(event_time)
        with connection.cursor() as cursor:
            sql = "INSERT INTO sensor (temp, humi, sound, tilt, vibrate, fire, smoke, light_sense, event_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (temp, humi, sound, tilt, vibrate, fire, smoke, light_sense, event_time))
        connection.commit()
        print('字段插入成功')
    except:
        print('字段插入失败')
    finally:
        connection.close()


@app.route('/sensor_datas', methods=['POST'])
def sensor_datas():
    data = request.get_json()
    select_sensors = data.get('sensors', [])  # 修改为列表，以支持多个传感器
    sensor_num = data.get('sensor_num', 10)  # 修改为更通用的变量名，并设置默认值

    # 构建完整的SQL查询语句
    sql = f"SELECT {select_sensors}, event_time FROM sensor ORDER BY event_time DESC LIMIT {sensor_num};"

    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            result = {'temp': str(random.randint(20, 25)), 'humi': str(random.randint(20, 30)),
                           'sound': str(random.choice([0, 1])), 'tilt': str(random.choice([0, 1])),
                           'vibrate': str(random.choice([0, 1])), 'fire': str(random.choice([0, 1])),
                           'smoke': str(random.randint(0, 255)), 'light_sense': str(random.randint(0, 255)),
                           'event_time': '1000058680'}
            # {'temp': '81', 'humi': '0', 'sound': '0', 'tilt': '0', 'vibrate': '0', 'fire': '0', 'smoke': '156', 'light_sense': '116', 'event_time': '20241207T171738Z'}
            print(result)
            return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': '2', "error": str(e)}), 500
    finally:
        connection.close()

@app.route('/sensor_items', methods=['POST'])
def sensor_items():
    sensor_fields = {
    "temp": "温度",
    "humi": "湿度",
    "sound": "声音",
    "tilt": "倾斜",
    "vibrate": "振动",
    "fire": "火焰",
    "smoke": "烟雾",
    "light_sense": "光敏",
    }
    data = request.get_json()
    select_sensors = data.get('sensors', [])  # 修改为列表，以支持多个传感器
    sensor_num = data.get('sensor_num', 10)  # 修改为更通用的变量名，并设置默认值
    value_sensor = sensor_fields[select_sensors]
    # 构建完整的SQL查询语句
    sql = f"SELECT {select_sensors}, event_time FROM sensor ORDER BY event_time DESC LIMIT {sensor_num};"

    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            for item in result:
                    # 将'temp'键的值赋给'temperature'键
                    item['dataItem'] = item[select_sensors]
                    # 删除'temp'键（可选，取决于你是否还想保留它）
                    del item[select_sensors]
            analyse = t3.all_result(select_sensors, {'subscriptions':result})
            # result = str(result).replace(select_sensors, 'dataitem')
            # {'subscriptions': [{'temp': '108', 'event_time': '1000000999'}, {'temp': '160', 'event_time': '1000000998'}, {'temp': '186', 'event_time': '1000000997'}, {'temp': '170', 'event_time': '1000000996'}, {'temp': '158', 'event_time': '1000000995'}, {'temp': '191', 'event_time': '1000000994'}, {'temp': '132', 'event_time': '1000000993'}, {'temp': '168', 'event_time': '1000000992'}, {'temp': '137', 'event_time': '1000000991'}, {'temp': '130', 'event_time': '1000000990'}]}
            print({'subscriptions': result, 'value':[value_sensor], 'analyse': analyse})
            return jsonify({'subscriptions': result, 'value':[value_sensor], 'analyse': analyse}), 200
    except Exception as e:
        return jsonify({'message': '2', "error": str(e)}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    with app.app_context():
        scheduler.add_job(
            id='my_scheduled_task_job',
            func=save_data,
            trigger='interval',
            minutes=1000,

        )
    app.run(debug=True)
    ''''
    1000059580
    1734675921
    https://atomgit.com/space_station_environmental_moni/000053/i
    git remote add origin https://atomgit.com/space_station_environmental_moni/000053.git
    atp_ly2o48yq93a64gmmbmiuitdid1qdudwn
    git -c http.extraheader="Authorization: Basic $(echo -n atp_ly2o48yq93a64gmmbmiuitdid1qdudwn: | base64)" pull
    https://atomgit.com/space_station_environmental_moni/000053.git

    '''