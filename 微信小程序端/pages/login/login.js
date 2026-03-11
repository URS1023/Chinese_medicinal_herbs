// login.js
Page({
  data: {
    username: '',
    password: ''
  },
  // 输入用户名
  onUsernameInput: function (e) {
    this.setData({
      username: e.detail.value
    })
  },
  // 输入密码
  onPasswordInput: function (e) {
    this.setData({
      password: e.detail.value
    })
  },
  // 登录
  onLogin: function () {
    const { username, password } = this.data
    if (username && password) {
      // 这里应该是调用实际的登录API
      wx.request({
        url: 'http://127.0.0.1:5000/login',
        data:{
          'username': username,
          'password': password,
          'remember': 'off'
        },
        method:'POST',
        header: {
          'content-type': 'application/json'
        },
        success: function (res) {
          console.log(res.statusCode)
          if(res.statusCode==200){
            console.log('登录成功')
            wx.showToast({
              title: '登录成功',
              icon: 'success',
              duration: 2000
            })
            // 登录成功后的操作，比如跳转到首页
            wx.switchTab({
              url: '/pages/index/index'
            })
            console.log(1123)
          }else if(res.statusCode==400){
          wx.showToast({
            title: '输入信息不完整',
            icon: 'none',
            duration: 2000
            })
          }else if(res.statusCode==500){
              wx.showToast({
                title: '登录失败',
                icon: 'none',
                duration: 2000
                })
          }else if(res.statusCode==401){
            wx.showToast({
              title: '用户名或密码错误',
              icon: 'none',
              duration: 2000
              })
        }
        }
      })
    } else {
      wx.showToast({
        title: '请输入用户名和密码',
        icon: 'none',
        duration: 3000
      })
    }
  },
  // 注册
  onRegister: function () {
    wx.navigateTo({
      url: '/pages/register/register'
    })
  },
  // 忘记密码
  onForgotPassword: function () {
    wx.showModal({
      title: '忘记密码',
      content: '请联系管理员重置密码',
      showCancel: false
    })
  }
})
