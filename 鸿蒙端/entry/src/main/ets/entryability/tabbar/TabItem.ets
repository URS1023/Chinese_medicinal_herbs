export interface TabItem {
  icon:Resource;
  icon_selected:Resource
  title: String;
  id: number;

}
export  enum TabID{
  HOURSE,
  Device_information,
  solar_energy,
  MINE
}
export const TabItemsList: TabItem[] = [
  {
    icon:$r('app.media.ic1'),
    icon_selected:$r('app.media.ic1'),
    title:String('数据展示'),
    id:TabID.HOURSE
  },
  {
    icon:$r('app.media.ic2'),
    icon_selected:$r('app.media.ic2'),
    title:String('设备信息'),
    id:TabID.Device_information
  },
  {
    icon:$r('app.media.ic3'),
    icon_selected:$r('app.media.ic3'),
    title:String('太阳能'),
    id:TabID.solar_energy
  },
  {
  icon:$r('app.media.ic4'),
  icon_selected:$r('app.media.ic4'),
  title:String('我的'),
  id:TabID.MINE
},
]