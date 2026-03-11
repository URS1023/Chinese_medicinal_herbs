// index.js
const app = getApp()
Page({
  data: {
    bannerList: [], // 轮播图数据
    // categoryList: [], // 分类导航数据
    announcementList: [] // 公告资讯数据
  },
  onLoad: function () {
    this.loadBannerData()
    // this.loadCategoryData()
    this.loadAnnouncementData()
  },
  // 加载轮播图数据
  loadBannerData: function () {
    // 这里应该是从本地JSON文件或API获取数据，为了演示，我们使用模拟数据
    this.setData({
      bannerList: [
        {
          id: 1,
          image: '/images/picture/三七.jpg',
          text: "三七"
        },
        {
          id: 2,
          image: '/images/picture/丹参.jpg',
          text: '丹参'
        },
        {
          id: 3,
          image: '/images/picture/人参.jpg',
          text: '人参'
        }
      ]
    })
  },
  // 加载公告资讯数据
  loadAnnouncementData: function () {
    this.setData({
      announcementList: [
        { id: 1, title: '小程序更新，新增药材查询功能', date: '2024-09-01' },
        { id: 2, title: '中药材知识讲座即将开课', date: '2024-08-28' },
        { id: 3, title: '关注我们，获取最新资讯', date: '2024-08-25' }
      ]
    })
  },
  // 搜索功能
  onSearch: function (e) {
    const searchValue = e.detail.value
    console.log('搜索：', searchValue)
    // 这里应该根据搜索值跳转到搜索结果页面
    wx.navigateTo({
      url: '/pages/list/list?searchValue=' + searchValue
    })
  },
  // 轮播图点击事件
  onBannerTap: function (e) {
    const bannerId = e.currentTarget.dataset.id
    console.log('点击了轮播图：', bannerId)
    // 这里应该跳转到商品详情页
    wx.navigateTo({
      url: '/pages/detail/detail?herbId=' + bannerId
    })
  },
  // 公告点击事件 (可以跳转到详情页)
  onAnnouncementTap: function (e) {
    const announcementId = e.currentTarget.dataset.id
    console.log('点击了公告：', announcementId)
    // TODO: 跳转到公告详情页
    // 可以创建一个新的页面来显示公告详情，例如 /pages/announcement-detail/announcement-detail
    wx.navigateTo({
      url: '/pages/announcement-detail/announcement-detail?id=' + announcementId
    })
  }
})

