import requests
import json

def get_token():
    # 定义请求的URL
    url = 'https://iam.cn-north-4.myhuaweicloud.com/v3/auth/tokens'
    # 定义请求头
    headers = {
    'Content-Type': 'application/json'
    }
    # "username”即IAM用户名、“password”即登录华为云密码、“domainname”即账号名，“projectname”项目
    # 密码应该是登录华为云的密码
    # 定义请求体
    payload = {
    "auth": {
        "identity": {
            "methods": [
                "password"
            ],
            "password": {
                "user": {
                    "domain": {
                        "name": "hid_celij2osg6h07m4"        #IAM用户所属帐号名
                    },
                    "name": "urd",             #IAM用户名
                    "password": "Zzzzllll3"      #IAM用户密码
                }
            }
        },
        "scope": {
            "project": {
                "name": "cn-north-4"               #项目名称
            }
        }
    }
    # VVLnmoTlh7rkuI3lhYs=
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    x_token = response.headers['X-Subject-Token']
    # print(x_token)
    return x_token
get_token()
# print("Status Code:", response.status_code)
# print("Response Body:", response.json())
