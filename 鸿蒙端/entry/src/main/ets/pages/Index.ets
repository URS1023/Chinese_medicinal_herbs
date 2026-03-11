import { promptAction, router } from '@kit.ArkUI'
import http from '@ohos.net.http'
class rouTmp{
  userNameParam:string=''
  passwordParam:string=''
}
const params: rouTmp = router.getParams() as rouTmp;
@Entry
@Component
struct Index {
  @State message: string = '中药材种植环境检测'
  @State userName: string = params.userNameParam;//用户名
  @State password: string = params.passwordParam;//密码

  build() {
    Row() {
      Column({space:6}) {
        Row(){
          Text(this.message)
            .fontSize(30)
            .fontWeight(FontWeight.Bold)
        }
        .margin({top:150})

        Image($r("app.media.3")).width(30)

        Column(){
          Row(){
            Image($r("app.media.3"))
              .width(30)
              .height(30)
            TextInput({placeholder:'请输入用户名：'}).width('80%')
              .onChange((value)=>{
                this.userName = value;
              })
          }
          .margin({top:100})

          Row(){
            Image($r("app.media.2"))
              .width(30)
              .height(30)
            TextInput({placeholder:'请输入密码：'}).width('80%').type(InputType.Password)
              .onChange((value)=>{
                this.password = value;
              })
          }.margin({top:10})
        }

        Row(){
          Button('注册账号')
            .controlSize(ControlSize.SMALL)
            .buttonStyle(ButtonStyleMode.TEXTUAL);
        }
        .width('90%')
        .justifyContent(FlexAlign.End)
        .onClick(()=>{
          router.pushUrl({
            url: 'pages/register',
            params: {
              userNameParam: this.userName,
              passwordParam: this.password,
            }
          })
        })


        Button('登陆')
          .width('40%')
          .onClick(()=>{
            if (this.userName != '' && this.password != '') {
              let httpRequest = http.createHttp();
              httpRequest.request(
                'http://127.0.0.1:5000/login',
                {
                  method:http.RequestMethod.POST,
                  extraData:{
                    'username': this.userName,
                    'password': this.password
                  },
                  header: {
                    'Content-Type': 'application/json'
                  }
                })
                .then(resp=>{
                  console.log("resp=>",JSON.stringify(resp))
                  if(resp.responseCode === 200){
                    console.log(resp.result.toString())
                    router.pushUrl({
                      url: 'pages/home',
                      params: {
                        userNameParam: this.userName,
                        passwordParam: this.password,
                      }
                    })
                  }else if (resp.responseCode === 401){
                    AlertDialog.show(
                      {
                        message: '账号密码错误',
                        autoCancel: true,
                        alignment: DialogAlignment.Bottom,
                        gridCount: 4,
                        offset: { dx: 0, dy: -20 },
                        primaryButton: {
                          value: 'cancel',
                          action: () => {
                            console.info('Callback when the first button is clicked')
                          }
                        }
                      })
                  }
                })
            }
            else {
              AlertDialog.show(
                {
                  message: '请输入账号密码',
                  autoCancel: true,
                  alignment: DialogAlignment.Bottom,
                  gridCount: 4,
                  offset: { dx: 0, dy: -20 },
                  primaryButton: {
                    value: 'cancel',
                    action: () => {
                      console.info('Callback when the first button is clicked')
                    }
                  }
                })
            }
          })
      }
      .height("100%")
    }
    .height('100%')
    .width("100%")
    .height('110%')
    .linearGradient({
      colors: [
        [0xffffff, 0.0], // 颜色断点1的颜色和比重，对应组件在180°方向上的起始位置
        [0xf56c6c, 1.0], // 颜色断点2的颜色和比重，对应组件在180°方向上的终点位置
      ]
    })
  }
}