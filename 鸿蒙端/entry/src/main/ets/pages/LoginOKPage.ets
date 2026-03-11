
import { McLineChart, Options } from '@mcui/mccharts'

@Entry
@Component
struct Index {
  // 初始化数据
  @State seriesOption: Options = new Options({
    xAxis:{
      data:['周一','周二','周三','周四','周五','周六','周日']
    },
    yAxis:{
      name:'温度'
    },
    series:[
      {
        name:'最高气温',
        data:[11, 11, 15, 13, 12, 130, 10]
      },
      {
        name:'最低气温',
        data:[1, -20, 2, 5, 3, 2, 0]
      }
    ]
  })
  // 动态修改数据
  aboutToAppear() {
    setTimeout(() => {
      // 传递需要修改的属性与数值，不需要全部传
      this.seriesOption.setVal({
        series:[
          {
            name:'最高气温',
            data:[110, 110, 150, 130, 120, 190, 100]
          }
        ]
      })
    }, 2000)
  }
  build() {
    Row() {
      McLineChart({
        options: this.seriesOption
      })
    }
    .height('50%')
  }
}