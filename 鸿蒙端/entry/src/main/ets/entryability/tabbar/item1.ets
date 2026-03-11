import getdata from '../../common/getdata';
import { promptAction, router } from '@kit.ArkUI'
import DeviceBean from '../../common/DeviceBean'

@Component
export struct DriveComponent1 {
  private timerId:number = 0;
  @State deviceBean : DeviceBean = getdata.getDeviceAll();
  build() {
    Column({ space: 8 }) {
      Text('数据展示')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .fontColor(Color.Orange)
        .margin({ top: 10 })
        .textAlign(TextAlign.Center)
      ColumnSplit() {
        Row() {
          Text('传感器').width('30%').height(50).textAlign(TextAlign.Start)
          Text('量化数据').width('30%').height(50).textAlign(TextAlign.Center)
        }
        .width('100%')
        .justifyContent(FlexAlign.Center)

        Row() {
          Text('温度大小').width('30%').height(50).textAlign(TextAlign.Start)
          Text(this.deviceBean.temperature.toString()).width('30%').height(50).textAlign(TextAlign.Center)
          Button('查看', { buttonStyle: ButtonStyleMode.NORMAL, role: ButtonRole.NORMAL })
        }
        .onClick(()=>{
          router.pushUrl({
            url: 'entryability/Datadisplay',
            params: {
              Sensor: "temp"
            }
          })
        })
        .width('100%')
        .justifyContent(FlexAlign.Center)

        Row() {
          Text('湿度大小').width('30%').height(50).textAlign(TextAlign.Start)
          Text(this.deviceBean.humidity.toString()).width('30%').height(50).textAlign(TextAlign.Center)
          Button('查看', { buttonStyle: ButtonStyleMode.NORMAL, role: ButtonRole.NORMAL })
          .onClick(()=>{
            router.pushUrl({
              url: 'entryability/Datadisplay',
              params: {
                Sensor: "humi"
              }
            })
          })
        }
        .width('100%')
        .justifyContent(FlexAlign.Center)

        Row() {
          Text('烟雾浓度').width('30%').height(50).textAlign(TextAlign.Start)
          Text(this.deviceBean.smokeAlarm.toString()).width('30%').height(50).textAlign(TextAlign.Center)
          Button('查看', { buttonStyle: ButtonStyleMode.NORMAL, role: ButtonRole.NORMAL })
            .onClick(()=>{
              router.pushUrl({
                url: 'entryability/Datadisplay',
                params: {
                  Sensor: "smoke"
                }
              })
            })

        }
        .width('100%')
        .justifyContent(FlexAlign.Center)

        Row() {
          Text('光照强度').width('30%').height(50).textAlign(TextAlign.Start)
          Text(this.deviceBean.lightSense.toString()).width('30%').height(50).textAlign(TextAlign.Center)
          Button('查看', { buttonStyle: ButtonStyleMode.NORMAL, role: ButtonRole.NORMAL })
            .onClick(()=>{
              router.pushUrl({
                url: 'entryability/Datadisplay',
                params: {
                  Sensor: "light_sense"
                }
              })
            })

        }
        .width('100%')
        .justifyContent(FlexAlign.Center)
      }
      .width('100%')
      .height('40%')

      Text('安全状态')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .fontColor(Color.Orange)
        .margin({ top: 10 })
        .textAlign(TextAlign.Center)
      ColumnSplit() {

        Row() {
          Text('异常监测').width('30%').height(50).textAlign(TextAlign.Start)
          Text('是/否').width('30%').height(50).textAlign(TextAlign.Center)
        }
        .width('100%')
        .justifyContent(FlexAlign.Center)
        Row(){
          Text('声音异常').width('30%').height(50).textAlign(TextAlign.Start)
          Text(this.deviceBean.soundLevel?"是":'否').width('30%').height(50).textAlign(TextAlign.Center)

          Button('查看', { buttonStyle: ButtonStyleMode.NORMAL, role: ButtonRole.NORMAL })
            .onClick(()=>{
              router.pushUrl({
                url: 'entryability/Datadisplay',
                params: {
                  Sensor: "sound"
                }
              })
            })
        }
        .width('100%')
        .justifyContent(FlexAlign.Center)

        Row(){
          Text('倾斜度异常').width('30%').height(50).textAlign(TextAlign.Start)
          Text(this.deviceBean.tiltAngle?"是":'否').width('30%').height(50).textAlign(TextAlign.Center)
          Button('查看', { buttonStyle: ButtonStyleMode.NORMAL, role: ButtonRole.NORMAL })
            .onClick(()=>{
              router.pushUrl({
                url: 'entryability/Datadisplay',
                params: {
                  Sensor: "tilt"
                }
              })
            })
        }
        .width('100%')
        .justifyContent(FlexAlign.Center)

        Row(){
          Text('振动异常').width('30%').height(50).textAlign(TextAlign.Start)
          Text(this.deviceBean.vibrationIntensity?"是":'否').width('30%').height(50).textAlign(TextAlign.Center)
          Button('查看', { buttonStyle: ButtonStyleMode.NORMAL, role: ButtonRole.NORMAL })
            .onClick(()=>{
              router.pushUrl({
                url: 'entryability/Datadisplay',
                params: {
                  Sensor: "vibrate"
                }
              })
            })
        }
        .width('100%')
        .justifyContent(FlexAlign.Center)

        Row(){
          Text('火焰监测').width('30%').height(50).textAlign(TextAlign.Start)
          Text(this.deviceBean.fireAlarm?"是":'否').width('30%').height(50).textAlign(TextAlign.Center)
          Button('查看', { buttonStyle: ButtonStyleMode.NORMAL, role: ButtonRole.NORMAL })
            .onClick(()=>{
              router.pushUrl({
                url: 'entryability/Datadisplay',
                params: {
                  Sensor: "fire"
                }
              })
            })
        }
        .width('100%')
        .justifyContent(FlexAlign.Center)
      }
      .width('100%')
      .height('40%')
    }
    .width('100%')
    .height("100%")

  }
  loadDeviceData(){

    this.deviceBean = getdata.getDeviceAll();
    // console.log(this.deviceBean.temperature)
  }
  aboutToAppear(){
    this.loadDeviceData()
    this.timerId = setInterval(()=>{
      this.loadDeviceData();
    },3000)
  }

}
