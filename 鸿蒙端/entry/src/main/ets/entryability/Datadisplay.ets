import { router } from '@kit.ArkUI'
import http from '@ohos.net.http'
import { McBarChart, McLineChart, Options } from '@mcui/mccharts'

export class MyUser {
  analyse: analyse[]=[]
  subscriptions: Subscriptions[]=[]
  value: string = ''
}

export class Subscriptions {
  dataItem: string = ''
  event_time: string = ''
}
export class analyse {
  value: string = ''
}
class rouTmp{
  Sensor:string=''
}
const params: rouTmp = router.getParams() as rouTmp;
console.log(params.Sensor)

@Entry
@Component
struct LoginOKPage {
  @State seriesOption: Options = new Options({
  })

  @State myUser: MyUser = null!
  @State message: string = '历史数据'
  @State message1: string = ''
  @State message2: string = ''
  @State message3: string = ''
  @State message4: string = ''
  @State message5: string = ''
  @State isVisible: number = 1;

  build() {
    Navigation() {
      Row() {
        Column() {

          Text(this.message)
            .fontSize(24)
            .fontWeight(FontWeight.Bold)
            .fontColor(Color.Black)
            .margin({top: 0})



          if (this.isVisible == 1) {
            McLineChart({
              options: this.seriesOption
            })
              .width('90%')
              .height('50%')
          }
          if (this.isVisible == 2) {
            McBarChart({
              options: this.seriesOption
            })
              .width('90%')
              .height('50%')
          }

          Row() {
            Button('折线图', { buttonStyle: ButtonStyleMode.TEXTUAL, role: ButtonRole.NORMAL })
              .onClick(() => {
                this.isVisible = 1
              })
            Button('柱状图', { buttonStyle: ButtonStyleMode.TEXTUAL, role: ButtonRole.NORMAL })
              .onClick(() => {
                this.isVisible = 2
              })
          }
          .justifyContent(FlexAlign.End)
          .width('100%')

          Column()
          Row(){
            Text('数据分析')
              .fontSize(24)
              .fontWeight(FontWeight.Bold)
              .fontColor(Color.Black)
          }
          .height(50)
          .width('100%')
          .justifyContent(FlexAlign.Center)

          Swiper() {
              Text(this.message1)
                .width('90%')
                .height(160)
                .textAlign(TextAlign.Center)

              Text(this.message2)
                .width('90%')
                .height(160)
                .textAlign(TextAlign.Center)

              Text(this.message3)
                .width('90%')
                .height(160)
                .textAlign(TextAlign.Center)

              Text(this.message4)
                .width('90%')
                .height(160)
                .textAlign(TextAlign.Center)

              Text(this.message5)
                .width('90%')
                .height(160)
                .textAlign(TextAlign.Center)

          }

          .cachedCount(2)
          .index(1)
          .autoPlay(true)
          .interval(4000)
          .indicator(Indicator.digit() // 设置数字导航点样式
            .top(200)
            .fontColor(Color.Gray)
            .selectedFontColor(Color.Gray)
            .digitFont({ size: 20, weight: FontWeight.Bold })
            .selectedDigitFont({ size: 20, weight: FontWeight.Normal }))
          .loop(true)
          .duration(1000)
          .itemSpace(0)
          .displayArrow(true, false)



        }
        .width('100%')
        .height('100%')
      }
      .height('100%')
    }
    .size({width: '100%', height: '100%'}) // Navigation只设置了size，没有设置任何其它属性
    .titleMode(NavigationTitleMode.Mini)   //设置标题模式
    .title('历史数据')

  }

  onPageShow() {
    let httpRequest = http.createHttp();
    httpRequest.request(
      'http://127.0.0.1:5000/sensor_items',
      {
        method: http.RequestMethod.POST,
        extraData: {
          'sensors': params.Sensor,
          'sensor_num': 7
        },
        header: {
          'Content-Type': 'application/json'
        }
      })
      .then(resp => {
        if (resp.responseCode === 200) {
          console.log(resp.result.toString())
          this.myUser = JSON.parse(resp.result.toString());
          const analyse = this.myUser.analyse
          this.message1 = analyse[0].value.toString()
          this.message2 = analyse[1].value.toString()
          this.message3 = analyse[2].value.toString()
          this.message4 = analyse[3].value.toString()
          this.message5 = analyse[4].value.toString()
          const subscriptions = this.myUser.subscriptions;
          // console.log(this.myUser.subscriptions)
          let aac:string[] = []
          let bbd:string[] = []
          subscriptions
            .forEach((subscription, index) => {
              let a = subscription.event_time.toString()
              let b = subscription.dataItem.toString()
              aac.push(b)
              let date = new Date(Number(a + '000'));
              date.toTimeString().substring(0,5)
              bbd.push(date.toLocaleDateString().substring(2,8) + ' ' + date.toTimeString().substring(0,5))

            })
          this.seriesOption.setVal({
            series: [
              {
                name:this.myUser.value[0].toString(),
                data:aac
              },
            ],
            xAxis:{
              data:bbd
            },
            yAxis:{
              name:this.myUser.value
            },
          })
        }
      })
    // console.log(event_time_data_json[1], 1123)
    // console.log(Sensordata_data_json.toString())

}
}