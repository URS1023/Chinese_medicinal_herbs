// 定义电池信息接口
interface BatteryInfo {
  capacity: number;  // 电池容量
  level: number;  // 电池电量水平
  chargingStatus: boolean;  // 是否正在充电
}

@Component
export  struct DriveComponent5 {
  // 模拟电池信息数据
  @State batteryInfo: BatteryInfo = {
    capacity: 100,  // 初始容量设为 100（可根据实际情况调整单位）
    level: 50,  // 初始电量水平设为 50%
    chargingStatus: false
  };

  // 模拟太阳能板状态
  @State solarPanelActive: boolean = false;  // 是否开启太阳能板

  // 切换太阳能板状态的函数
  toggleSolarPanel() {
    this.solarPanelActive =!this.solarPanelActive;
  }

  build() {
    Column() {
      // 电池信息部分
      Column() {
        Text('电池储能信息').fontSize(20).fontWeight(500).margin({ bottom: 10 })
        Text('容量: '+ this.batteryInfo.capacity).margin({ bottom: 5 })
        Text('电量: '+ this.batteryInfo.level + '%').margin({ bottom: 5 })
        Text('充电状态: '+ (this.batteryInfo.chargingStatus? '充电中' : '未充电')).margin({ bottom: 10 })
      }.width('100%').margin({ bottom: 20 })

      // 太阳能板控制部分
      Column() {
        Text('太阳能板控制').fontSize(20).fontWeight(500).margin({ bottom: 10 })
        if (this.solarPanelActive) {
          Text('太阳能板已开启').margin({ bottom: 5 })
        } else {
          Text('太阳能板已关闭').margin({ bottom: 5 })
        }
        Button('切换太阳能板状态')
          .width('80%')
          .height(50)
          .margin({ top: 10 })
          .onClick(() => {
            this.toggleSolarPanel();
          })
      }.width('100%').margin({top: 50})

      // 这里可以添加更多功能组件，比如实时监测数据更新的图表展示区域（预留位置）
      //...

    }.width('100%').height('100%').backgroundColor('#f1f2f3')
  }
}
