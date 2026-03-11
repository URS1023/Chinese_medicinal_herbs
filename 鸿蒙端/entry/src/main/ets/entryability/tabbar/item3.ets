@Component
export  struct DriveComponent3 {

  build(){
    Column() {
      Text('个人资料')
        .fontStyle(100)
        .height(100)
        .margin(15)
        .fontSize(24)
        .fontColor(Color.Black)
        .fontWeight(FontWeight.Bold)
      Column({space:8}) {
        Row() {
          Row() {
            Image($r('app.media.user_'))
              .width(28)
              .height(28)
            Text('头像')
              .fontSize(20)
              .margin(6)
          }

          Image($r('app.media.right'))
            .width(38)
            .height(38)
        }
        .width('100%')
        .justifyContent(FlexAlign.SpaceBetween)

        Row() {
          Row() {
            Image($r('app.media.id'))
              .width(28)
              .height(28)
            Text('ID')
              .fontSize(20)
              .margin(6)
          }
          Text('001')
            .fontSize(20)
            .margin(10)
        }
        .width('100%')
        .justifyContent(FlexAlign.SpaceBetween)

        Row() {
          Row() {
            Image($r('app.media.nick'))
              .width(28)
              .height(28)
            Text('昵称')
              .fontSize(20)
              .margin(6)
          }
          Text('UR的出不克')
            .fontSize(20)
            .margin(10)
        }
        .width('100%')
        .justifyContent(FlexAlign.SpaceBetween)
      }
      .width('100%')
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#f1f2f3')

  }
}