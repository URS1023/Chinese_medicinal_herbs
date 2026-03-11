Page({
  data: {
    announcement: null
  },
  onLoad: function (options) {
    const allAnnouncementData = [
      {
        id: 1,
        title: "小程序更新，新增药材查询功能",
        date: "2025-05-01",
        content: "尊敬的用户，我们很高兴地宣布，小程序已完成重大更新！现在您可以更便捷地查询各类中药材的详细信息，包括药性、功效、用法用量等。我们致力于为您提供更优质的服务和更全面的中药材知识。感谢您的支持！"
      },
      {
        id: 2,
        title: "中药材知识讲座即将开课",
        date: "20245-05-28",
        content: "为了普及中药材知识，我们特邀资深中医药专家举办线上讲座。本次讲座将深入浅出地讲解常见中药材的识别、功效和应用，欢迎广大中药爱好者积极参与。具体时间和报名方式请关注后续通知。"
      },
      {
        id: 3,
        title: "关注我们，获取最新资讯",
        date: "2025-05-25",
        content: "如果您想第一时间获取中药材行业的最新资讯、健康养生知识和我们的活动信息，请务必关注我们的小程序。我们将定期更新高质量内容，助您更好地了解中医药文化，享受健康生活。"
      }
    ]

    const announcementId = parseInt(options.id) // 获取从上一页传递过来的公告ID
    this.loadAnnouncementDetail(announcementId, allAnnouncementData)
  },
  loadAnnouncementDetail: function (id, data) {
    const announcement = data.find(item => item.id === id)
    if (announcement) {
      this.setData({ announcement })
    } else {
      console.error('未找到对应的公告信息，ID：', id)
      // 可以添加错误处理，例如跳转回首页或列表页
    }
  }
}) 