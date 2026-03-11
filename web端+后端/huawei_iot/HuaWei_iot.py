from huawei_iot.t1 import get_token
import json
import requests
a = {
    "device_id": "6749b788ef99673c8ad11961_hi3861_led",
    "shadow": [
        {
            "service_id": "attribute",
            "desired": {
                "properties": 'null',
                "event_time": 'null'
            },
            "reported": {
                "properties": {
                    "led": "OFF",
                    "temperature": 0,
                    "temp": 81,
                    "humi": 0,
                    "sound": 0,
                    "tilt": 0,
                    "vibrate": 0,
                    "fire": 0,
                    "smoke": 156,
                    "light_sense": 116
                },
                "event_time": "20241207T171738Z"
            },
            "version": 2295
        }
    ]
}
def re_data():
    x_token = get_token()

    url = "https://66b9f3986d.st1.iotda-app.cn-north-4.myhuaweicloud.com/v5/iot/7083399e806f42c0b51a5c072d1af8e8/devices/6749b788ef99673c8ad11961_hi3861_led/shadow"

    payload = ""
    headers = {
        'Content-Type': 'application/json,charset=UTF-8',
        'X-Auth-Token': x_token
    }

    response = requests.request("get", url, headers=headers, data=payload)
    json_data = json.loads(response.text)
    properties = json_data['shadow'][0]['reported']['properties']
    event_time = json_data['shadow'][0]['reported']['event_time']
    led = properties['led']
    temp = properties['temp']
    humi = properties['humi']
    sound = properties['sound']
    tilt = properties['tilt']
    vibrate = properties['vibrate']
    fire = properties['fire']
    smoke = properties['smoke']
    light_sense = properties['light_sense']
    print(led, temp, humi, sound, tilt, vibrate, fire, smoke, light_sense, event_time)
    return led, temp, humi, sound, tilt, vibrate, fire, smoke, light_sense, event_time
if __name__ == '__main__':
    re_data()
'''
{
    "device_id": "6749b788ef99673c8ad11961_hi3861_led",
    "shadow": [
        {
            "service_id": "attribute",
            "desired": {
                "properties": null,
                "event_time": null
            },
            "reported": {
                "properties": {
                    "led": "OFF",
                    "temperature": 0,
                    "temp": 81,
                    "humi": 0,
                    "sound": 0,
                    "tilt": 0,
                    "vibrate": 0,
                    "fire": 0,
                    "smoke": 156,
                    "light_sense": 116
                },
                "event_time": "20241207T171738Z"
            },
            "version": 2295
        }
    ]
}
'''



