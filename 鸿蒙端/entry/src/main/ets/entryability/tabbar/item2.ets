interface SensorData {
  temp: string;
  humi: string;
  smoke: string;
  light: string;
  sound: string;
  tilt: string;
  vibrate: string;
  fire: string;
}
@Component
export  struct DriveComponent2 {
  @State sensorDataList: SensorData[] = [
    {
      temp: 'int',
      humi: 'int',
      smoke: 'int',
      light: 'int',
      sound: 'boolean',
      tilt: 'boolean',
      vibrate: 'boolean',
      fire: 'boolean'
    }
  ];

    build(){
      Column({space:8}){
        Text('设备信息')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .fontColor(Color.Orange)
        .margin({top:10})
        ColumnSplit(){
            Row(){
              Text('设备列表').width('30%').height(50).textAlign(TextAlign.Center).width('50%')
              Button('增加设备', { buttonStyle: ButtonStyleMode.NORMAL, role: ButtonRole.NORMAL }).margin({left: 80})
            }
            .width('100%')
          Row(){
            Text('设备名称').width('30%').height(50).textAlign(TextAlign.Center).width('50%')
            Text('设备ID').width('30%').height(50).textAlign(TextAlign.Center).width('50%')
          }
          .width('90%')
            Row(){
              Text('环境监测装置')
                .height(50)
                .textAlign(TextAlign.Center)
                .fontSize(15)
                .width('50%')
              Text('hi3861_environment')
                .height(50)
                .textAlign(TextAlign.Center)
                .fontSize(15)
            }
            .width('100%')

        }
        .width('100%')
        .height('20%')
        Divider().width('100%').height(2).backgroundColor(0xCCCCCC).margin({top: 20})

        Row() {
          // 表头行
          Column({space: 10}) {
            Text('属性名称').width('40%').height(30)
            Text('温度').width('20%').height(30)
            Text('湿度').width('20%').height(30)
            Text('烟雾').width('20%').height(30)
            Text('光敏').width('20%').height(30)
            Text('声音').width('20%').height(30)
            Text('倾斜').width('20%').height(30)
            Text('振动').width('20%').height(30)
            Text('火焰').width('20%').height(30)
          }.width('50%').margin({ left: 5 })

          // 数据列
          Column() {
            Text('属性字段').width('50%').height(30)
            ForEach(this.sensorDataList, (sensorDataItem: SensorData) => {
              Column({space: 10}) {
                Text('' + sensorDataItem.temp).width('30').height(30)
                Text('' + sensorDataItem.humi).width('30%').height(30)
                Text('' + sensorDataItem.smoke).width('30%').height(30)
                Text('' + sensorDataItem.light).width('30%').height(30)
                Text('' + sensorDataItem.sound).width('70%').height(30)
                Text('' + sensorDataItem.tilt).width('70%').height(30)
                Text('' + sensorDataItem.vibrate).width('70%').height(30)
                Text('' + sensorDataItem.fire).width('70%').height(30)
              }.width('50%')
            }, (sensorDataItem: SensorData, index: number) => {
              return `${sensorDataItem.temp}-${index}`;
            })
          }.width('50%')
        }
        .width('100%')
        .margin({top: 30})



      }
    .width('100%')
    .height('100%')
    .backgroundColor('#f1f2f3')
  }

}