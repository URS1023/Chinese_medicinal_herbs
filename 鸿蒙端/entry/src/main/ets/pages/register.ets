import { promptAction, router } from '@kit.ArkUI'
import http from '@ohos.net.http'

@Entry
@Component
struct Index {
  @State message: string = '注册账号'
  @State userName: string = '';//用户名
  @State password: string = '';//密码
  @State passwordagain: string = '';//密码

  build() {
    Row() {
      Column({space:6}) {
        Row(){
          Text(this.message)
            .fontSize(50)
            .fontWeight(FontWeight.Bold)
        }
        .margin({top:150})

        Image($r("app.media.3")).width(30)

        Column(){
          Row(){
            Image($r("app.media.2"))
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
            TextInput({placeholder:'请输入密码：'}).width('80%')
              .onChange((value)=>{
                this.password = value;
              })
          }.margin({top:10})
          Row(){
            TextInput({placeholder:'再次输入密码：'}).width('80%')
              .onChange((value)=>{
                this.passwordagain = value;
              })
              .margin({left:30})
          }.margin({top:10})
        }


        Button('注册')
          .width('40%')
          .onClick(()=>{
            if (this.password != this.passwordagain){
              AlertDialog.show(
                {
                  message: '两次密码不匹配',
                  autoCancel: true,
                  alignment: DialogAlignment.Bottom,
                  gridCount: 4,
                  offset: { dx: 0, dy: -20 },
                })
            }
            else if (this.userName != '' && this.password != '') {
              let httpRequest = http.createHttp();
              httpRequest.request(
                'http://127.0.0.1:5000/register',
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
                  if(resp.responseCode === 201){
                    console.log(resp.result.toString())
                    router.back({
                      url: 'pages/Index',
                      params: {
                        userNameParam: this.userName,
                        passwordParam: this.password,
                      }
                    })
                  }
                  else if(resp.responseCode === 400){
                    AlertDialog.show(
                      {
                        message: '用户已存在',
                        autoCancel: true,
                        alignment: DialogAlignment.Bottom,
                        gridCount: 4,
                        offset: { dx: 0, dy: -20 },
                      })
                  }else{
                    AlertDialog.show(
                      {
                        message: '注册失败',
                        autoCancel: true,
                        alignment: DialogAlignment.Bottom,
                        gridCount: 4,
                        offset: { dx: 0, dy: -20 },
                      })
                  }
                })
            }else{
              AlertDialog.show(
                {
                  message: '请输入密码',
                  autoCancel: true,
                  alignment: DialogAlignment.Bottom,
                  gridCount: 4,
                  offset: { dx: 0, dy: -20 },
                })
            }
          })
          .margin({top:30})
        Button('返回登录')
          .onClick(()=>{
            router.back({
              url: "pages/Index",
              params: {
                userNameParam: this.userName,
                passwordParam: this.password,
              }
            })
          })
          .width('40%')


      }
      .height("100%")
    }
    .height('100%')
    .width("100%")
    .height('110%')
    .linearGradient({

      colors: [
        [0xffffff, 0.0],
        [0xf56c6c, 1.0],
      ]
    })
  }
}