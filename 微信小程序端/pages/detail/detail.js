// detail.js
Page({
  data: {
    herb: null
  },
  onLoad: function (options) {
    const herbId = options.herbId
    this.loadHerbDetail(herbId)
  },
  // 加载中药材详情
  loadHerbDetail: function (herbId) {
    // 这里应该是从本地JSON文件或API获取数据，为了演示，我们使用模拟数据
    const herb = {
      id: herbId,
      name: '黄芪',
      image: '/images/picture/黄芪.jpg',
      description: '黄芪，又名黄耗子、芪芍药，为五加科植物乌头的干燥根茎。',
      properties: '滋补养生，清热解毒',
      usage: '内服：煎汤，10-20g；或入散剂。外用：捣敷或贴患处。',
      dosage: '轻症患者早晚各服1剂，连用7-10天。重症患者可适当加量，具体用量与症状相适应。'
    }
    this.setData({ herb })
  },
  // 收藏功能
  onCollectTap: function () {
    wx.showToast({
      title: '收藏成功',
      icon: 'success',
      duration: 2000
    })
  },
  // 分享功能
  onShareTap: function () {
    wx.showShareMenu({
      withShareTicket: true,
      menus: ['shareAppMessage', 'shareTimeline']
    })
  }
})
