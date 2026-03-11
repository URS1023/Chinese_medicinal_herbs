import DeviceBean from '../common/DeviceBean'
import http from '@ohos.net.http'
export class getdata {
  public getDeviceItem(sensors: string, sensor_num: number) : DeviceBean {
    let deviceBean = new DeviceBean(0, 0, 0, 0, 0, 0, 0, 0, '0');
    let httpRequest = http.createHttp();
    httpRequest.request(
      'http://127.0.0.1:5000/api/sensor/realtime',
      {
        method: http.RequestMethod.POST,
        extraData: {
          'sensors': sensors,
          'sensor_num': sensor_num
        },
        header: {
          'Content-Type': 'application/json'
        }
      })
      .then(resp => {
        console.log(resp.responseCode.toString(), '1123')
        console.log("resp=>", JSON.stringify(resp))
        if (resp.responseCode === 200) {
          console.log(resp.result.toString())
        }
        // deviceBean.temperator = deviceBean.temperator+Math.floor(Math.random()*5)

      })
    return deviceBean
  }
  // temp, humi, sound, tilt, vibrate, fire, smoke, light_sense, event_time
  public getDeviceAll() : DeviceBean  {
    interface sensor {
      temp: number,
      humi: number,
      sound: number,
      tilt: number,
      vibrate: number,
      fire: number,
      smoke: number,
      light_sense: number,
      event_time: string
    }
    let deviceBean = new DeviceBean(0, 0, 0, 0, 0, 0, 0, 0, '0');
    let httpRequest = http.createHttp();
    httpRequest.request(
      'http://127.0.0.1:5000/api/sensor/realtime',
      {
        method: http.RequestMethod.POST,
        extraData: {
          'sensors': "temp, humi, sound, tilt, vibrate, fire, smoke, light_sense",
          'sensor_num': "1"
        },
        header: {
          'Content-Type': 'application/json'
        }
      })
      .then(resp => {
        if (resp.responseCode === 200) {
          // console.log(resp.result.toString());
          let person:sensor=JSON.parse(resp.result.toString())as sensor;
          deviceBean.temperature = person.temp
          deviceBean.humidity = person.humi
          deviceBean.soundLevel = person.sound
          deviceBean.tiltAngle = person.tilt
          deviceBean.vibrationIntensity = person.vibrate
          deviceBean.fireAlarm = person.fire
          deviceBean.smokeAlarm = person.smoke
          deviceBean.lightSense = person.light_sense
          deviceBean.eventTime = person.event_time
        }
        // console.log(deviceBean.eventTime);
      })
    return deviceBean
  }
}
export default new getdata();
