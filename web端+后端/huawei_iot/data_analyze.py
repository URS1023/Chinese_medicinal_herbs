import json
import datetime

# 温度
def gentemp_temperature_report(data):
    # 将数据转换为更易于处理的格式
    temperature_records = []
    for record in data['subscriptions']:
        # 假设时间戳为毫秒级Unix时间戳
        try:
            timestamp = datetime.datetime.fromtimestamp(int(record['dataItem'])/1000)
        except ValueError:
            timestamp = record['dataItem']  # 如果转换失败，则保留原始值（这里不会执行，因为我们假设了格式）
        temperature = float(record['dataItem'])  # 将温度转换为浮点数
        temperature_records.append({'timestamp': timestamp, 'temperature': temperature})
    
    # 排序数据（按时间戳）
    temperature_records.sort(key=lambda x: x['timestamp'])
    
    # 计算一些基本的统计量
    avg_temperature = sum(record['temperature'] for record in temperature_records) / len(temperature_records)
    max_temperature = max(record['temperature'] for record in temperature_records)
    min_temperature = min(record['temperature'] for record in temperature_records)
    temperature_range = max_temperature - min_temperature
    

    # 假设的温度适宜范围（例如，对于居住或工作环境）
    DESIRED_TEMPERATURE_RANGE = (20.0, 24.0)  # 适宜温度范围：20°C 到 24°C

    report = ''
    for record in temperature_records:
        # 格式化时间戳为字符串
        timestamp_str = record['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        report += f"{timestamp_str}    {record['temperature']:.2f}\n"
    
    report = f"""
    1. **温度趋势**：
       - 最后一个温度数据点（{temperature_records[-1]['temperature']:.2f}°C）相对于前一个数据点（{temperature_records[-2]['temperature']:.2f}°C）是{'上升' if temperature_records[-1]['temperature'] > temperature_records[-2]['temperature'] else '下降'}的。
;
    2. **温度表现**：
       - 当前温度数据的平均值为{avg_temperature:.2f}°C，最高温度为{max_temperature:.2f}°C，最低温度为{min_temperature:.2f}°C。
;
    3. **温度波动**：
       - 温度的波动范围为{temperature_range:.2f}°C。
;
    4. **温度适宜度**：
       - 根据假设的适宜温度范围（{DESIRED_TEMPERATURE_RANGE[0]}°C 到 {DESIRED_TEMPERATURE_RANGE[1]}°C），当前温度数据中有{sum(1 for record in temperature_records if DESIRED_TEMPERATURE_RANGE[0] <= record['temperature'] <= DESIRED_TEMPERATURE_RANGE[1])}个数据点落在该范围内，占总数据点的{sum(1 for record in temperature_records if DESIRED_TEMPERATURE_RANGE[0] <= record['temperature'] <= DESIRED_TEMPERATURE_RANGE[1]) / len(temperature_records) * 100:.2f}%。
;
    5. **温度监控与调整**：
       - 如果温度频繁超出适宜范围，建议检查并调整温控系统，确保温度保持在适宜的范围内。
    """

    
    return report.split(';')

# 湿度
def gen_humidity_report(data):
    # 将数据转换为更易于处理的格式
    humidity_records = []
    for record in data['subscriptions']:
        try:
            timestamp = datetime.datetime.fromtimestamp(int(record['event_time']) / 1000)
            humidity = float(record['dataItem'])  # 直接使用数值，不进行百分比转换
        except (ValueError, KeyError):
            # 如果转换失败或数据不完整，则跳过该记录（或可以选择记录错误）
            continue
        humidity_records.append({'timestamp': timestamp, 'humidity': humidity})

    # 排序数据（按时间戳）
    humidity_records.sort(key=lambda x: x['timestamp'])

    # 计算一些基本的统计量
    avg_humidity = sum(record['humidity'] for record in humidity_records) / len(humidity_records)
    max_humidity = max(record['humidity'] for record in humidity_records)
    min_humidity = min(record['humidity'] for record in humidity_records)
    humidity_range = max_humidity - min_humidity

    # 假设的适宜湿度范围（直接使用数值范围）
    DESIRED_HUMIDITY_RANGE = (0.30, 0.60)  # 适宜湿度范围：例如，0.30到0.60（如果是百分比则对应30%到60%）
    # 注意：这里我们仍然用小数形式表示适宜范围，因为计算时使用的是小数

    report = ''
    for record in humidity_records:
        # 格式化时间戳为字符串
        timestamp_str = record['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        report += f"{timestamp_str}    {record['humidity']}\n"

    report = f"""
    1. **湿度趋势**：
       - 最后一个湿度数据点（{humidity_records[-1]['humidity']}）相对于前一个数据点（{humidity_records[-2]['humidity']}）是{'上升' if humidity_records[-1]['humidity'] > humidity_records[-2]['humidity'] else '下降'}的。
;
    2. **湿度表现**：
       - 当前湿度数据的平均值为{avg_humidity:2f}，最高湿度为{max_humidity}，最低湿度为{min_humidity}。
;
    3. **湿度波动**：
       - 湿度的波动范围为{humidity_range}。
;
    4. **湿度监控与调整**：
       - 如果湿度频繁超出适宜范围，建议检查并调整加湿或除湿系统，确保湿度保持在适宜的范围内。
;
    """

    return report.split(';')  # 返回按行分割的字符串列表

# 烟雾
def gen_smoke_report(data):
    # 将数据转换为更易于处理的格式
    smoke_records = []
    for record in data['subscriptions']:
        try:
            timestamp = datetime.datetime.fromtimestamp(int(record['event_time']) / 1000)
            smoke_concentration = float(record['dataItem'])  # 烟雾浓度值
        except (ValueError, KeyError):
            # 如果转换失败或数据不完整，则跳过该记录（或可以选择记录错误）
            continue
        smoke_records.append({'timestamp': timestamp, 'smoke': smoke_concentration})

    # 排序数据（按时间戳）
    smoke_records.sort(key=lambda x: x['timestamp'])

    # 计算一些基本的统计量
    avg_smoke = sum(record['smoke'] for record in smoke_records) / len(smoke_records)
    max_smoke = max(record['smoke'] for record in smoke_records)
    min_smoke = min(record['smoke'] for record in smoke_records)
    smoke_range = max_smoke - min_smoke

    # 假设的适宜烟雾浓度范围（根据实际应用场景设置）
    # 这里我们假设一个范围，但实际应用中这个范围应该根据具体情况来确定
    DESIRED_SMOKE_RANGE = (0, 50)  # 适宜烟雾浓度范围：例如，0到50（单位根据实际应用）

    report = ''

    report += f"""
    1. **烟雾浓度趋势**：
       - 最后一个烟雾浓度数据点（{smoke_records[-1]['smoke']}）相对于前一个数据点（{smoke_records[-2]['smoke']}）是{'上升' if smoke_records[-1]['smoke'] > smoke_records[-2]['smoke'] else '下降'}的。
;
    2. **烟雾浓度表现**：
       - 当前烟雾浓度的平均值为{avg_smoke:2f}，最高烟雾浓度为{max_smoke}，最低烟雾浓度为{min_smoke}。
;
    3. **烟雾浓度波动**：
       - 烟雾浓度的波动范围为{smoke_range}。
;
    4. **烟雾监控与调整**：
       - 如果烟雾浓度频繁超出适宜范围（{DESIRED_SMOKE_RANGE[0]}到{DESIRED_SMOKE_RANGE[1]}），建议检查并调整相关设备或采取相应措施，确保环境安全。
;
    """

    # 如果需要返回分割后的报告，可以使用split('\n\n')来按段落分割，但这里我们直接返回完整的报告字符串
    return report.split(';')

# 光敏
def gen_light_intensity_report(data):
    # 将数据转换为更易于处理的格式
    light_records = []
    for record in data['subscriptions']:
        try:
            timestamp = datetime.datetime.fromtimestamp(int(record['event_time']) / 1000)
            light_intensity = float(record['dataItem'])  # 光照强度值
        except (ValueError, KeyError):
            # 如果转换失败或数据不完整，则跳过该记录（或可以选择记录错误）
            continue
        light_records.append({'timestamp': timestamp, 'intensity': light_intensity})

    # 排序数据（按时间戳）
    light_records.sort(key=lambda x: x['timestamp'])

    # 计算一些基本的统计量
    avg_intensity = sum(record['intensity'] for record in light_records) / len(light_records)
    max_intensity = max(record['intensity'] for record in light_records)
    min_intensity = min(record['intensity'] for record in light_records)
    intensity_range = max_intensity - min_intensity

    # 假设的适宜光照强度范围（根据实际应用场景设置）
    # 这里我们假设一个范围，但实际应用中这个范围应该根据具体情况来确定
    DESIRED_INTENSITY_RANGE = (100, 300)  # 适宜光照强度范围：例如，100到300（单位：勒克斯或其他）

    report = ''


    report += f"""
    1. **光照强度趋势**：
       - 最后一个光照强度数据点（{light_records[-1]['intensity']}）相对于前一个数据点（{light_records[-2]['intensity']}）是{'上升' if light_records[-1]['intensity'] > light_records[-2]['intensity'] else '下降'}的。
;
    2. **光照强度表现**：
       - 当前光照强度的平均值为{avg_intensity:2f}，最高光照强度为{max_intensity}，最低光照强度为{min_intensity}。
;
    3. **光照强度波动**：
       - 光照强度的波动范围为{intensity_range}。
;
    4. **光照监控与调整**：
       - 如果光照强度频繁超出适宜范围（{DESIRED_INTENSITY_RANGE[0]}到{DESIRED_INTENSITY_RANGE[1]}），建议检查并调整照明系统，确保光照强度保持在适宜的范围内，以维护良好的视觉环境和能源效率。
;
    """

    # 如果需要返回分割后的报告，可以使用split('\n\n')来按段落分割，但这里我们直接返回完整的报告字符串
    return report.split(';')


def all_result(sensor_key, data):
    if sensor_key == "temp":
        analyse = gentemp_temperature_report(data)
    elif sensor_key == "humi":
        analyse = gen_humidity_report(data)
    elif sensor_key == "smoke":
        analyse = gen_smoke_report(data)
    elif sensor_key == "light_sense":
        analyse = gen_light_intensity_report(data)
    else:
        analyse = []
    nested_dict_list = [{'value': val} for val in analyse]

    return nested_dict_list


if __name__ == '__main__':
    data = {'subscriptions': [{'event_time': '1000059940', 'dataItem': '198'}, {'event_time': '1000059880', 'dataItem': '129'}, {'event_time': '1000059820', 'dataItem': '174'}, {'event_time': '1000059760', 'dataItem': '179'}, {'event_time': '1000059700', 'dataItem': '197'}, {'event_time': '1000059640', 'dataItem': '121'}, {'event_time': '1000059580', 'dataItem': '140'}]}
    report = gentemp_temperature_report(data)
    print(report)