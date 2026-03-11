// list.js
// 引入本地数据文件
const allHerbData = require('../../all_herb_data')

Page({
  data: {
    categoryId: null,
    searchValue: '', // 新增搜索值数据
    herbList: [],
    allHerbs: [], // 存储所有药材数据
    currentPage: 1,
    pageSize: 10
  },
  onLoad: function (options) {
    const categoryId = options.categoryId
    const searchValue = options.searchValue || '' // 获取搜索值
    this.setData({ categoryId, searchValue })
    // 加载所有药材数据
    this.setData({ allHerbs: allHerbData })
    this.loadHerbData(categoryId, searchValue)
  },
  // 加载中药材数据 (根据分类ID或搜索值筛选，目前暂不实现分类筛选)
  loadHerbData: function (categoryId, searchValue) {
    let filteredHerbs = this.data.allHerbs

    // 根据搜索值筛选药材
    if (searchValue) {
      const lowerCaseSearchValue = searchValue.toLowerCase()
      filteredHerbs = filteredHerbs.filter(herb => 
        herb.name.toLowerCase().includes(lowerCaseSearchValue) ||
        (herb.description && herb.description.toLowerCase().includes(lowerCaseSearchValue)) ||
        (herb.effects && herb.effects.toLowerCase().includes(lowerCaseSearchValue)) ||
        (herb.properties && herb.properties.toLowerCase().includes(lowerCaseSearchValue))
      )
    }

    // 暂时加载所有药材进行分页（或筛选后的药材进行分页）
    const initialHerbs = filteredHerbs.slice(0, this.data.pageSize)
    this.setData({
      herbList: initialHerbs,
      // 重置当前页和所有药材（如果进行了筛选）
      currentPage: 1,
      allHerbs: filteredHerbs // 更新 allHerbs 为筛选后的数据，以便分页加载
    })
  },
  // 跳转到中药材详情页
  onHerbTap: function (e) {
    const herbId = e.currentTarget.dataset.id
    wx.navigateTo({
      url: '/pages/detail/detail?herbId=' + herbId
    })
  },
  // 加载更多数据
  onReachBottom: function () {
    // 实现分页加载逻辑
    console.log('加载更多数据')
    const nextPage = this.data.currentPage + 1
    const startIndex = (nextPage - 1) * this.data.pageSize
    const endIndex = startIndex + this.data.pageSize
    const newHerbs = this.data.allHerbs.slice(startIndex, endIndex)

    if (newHerbs.length > 0) {
      this.setData({
        herbList: this.data.herbList.concat(newHerbs),
        currentPage: nextPage
      })
    } else {
      console.log('没有更多数据了')
    }
  }
}) 