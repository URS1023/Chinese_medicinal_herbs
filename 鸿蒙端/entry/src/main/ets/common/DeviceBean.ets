export default class DeviceBean {
  temperature: number; // 室内温度（原temp替换为temperature）
  humidity: number; // 室内湿度（原humi保留，但通常也写作humidity）
  soundLevel: number; // 声音级别（新增字段，对应sound）
  tiltAngle: number; // 倾斜角度（新增字段，对应tilt，假设为角度值）
  vibrationIntensity: number; // 振动强度（新增字段，对应vibrate）
  fireAlarm: number; // 火灾报警（新增字段，对应fire，使用布尔值表示是否触发）
  smokeAlarm: number; // 烟雾报警（新增字段，对应smoke，使用布尔值表示是否触发）
  lightSense: number; // 光线感应（新增字段，对应light_sense，可能是光照强度值）
  eventTime: string; // 事件时间（新增字段，对应event_time，使用Date类型）

  constructor(
    temperature: number,
    humidity: number,
    soundLevel: number,
    tiltAngle: number,
    vibrationIntensity: number,
    fireAlarm: number,
    smokeAlarm: number,
    lightSense: number,
    eventTime: string
  ) {
this.temperature = temperature;
    this.humidity = humidity;
    this.soundLevel = soundLevel;
    this.tiltAngle = tiltAngle;
    this.vibrationIntensity = vibrationIntensity;
    this.fireAlarm = fireAlarm;
    this.smokeAlarm = smokeAlarm;
    this.lightSense = lightSense;
    this.eventTime = eventTime;
  }
}