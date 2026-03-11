import { TabID, TabItemsList } from '../entryability/tabbar/TabItem';
import { DriveComponent1 } from '../entryability/tabbar/item1';
import { DriveComponent2 } from '../entryability/tabbar/item2';
import { DriveComponent3 } from '../entryability/tabbar/item3'
import { DriveComponent5 } from '../entryability/tabbar/item4'
@Entry
@Component
struct MainPage {
  @State pageIndex: number = 0
  private  tabController: TabsController = new TabsController();
  @State message: string = '系统主页'
  @Builder MyTabBuilder(idx: number){
    Column(){
      Image(idx === this.pageIndex ? TabItemsList[idx].icon_selected :
      TabItemsList[idx].icon)
        .width(32)
        .height(32)
      Text(TabItemsList[idx].title as string)
        .fontSize(14)
        .fontWeight(FontWeight.Bold)
        .fontColor(this.pageIndex === idx ? '#006eee':'#777')
    }
  }

  build() {

    Tabs({barPosition:BarPosition.End}){
      TabContent(){
        //Text('数据展示')
        DriveComponent1()
      }
      //.tabBar('数据展示')
      .tabBar(this.MyTabBuilder(TabID.HOURSE))

      TabContent() {
        //Text('设备信息')
        DriveComponent2()
      }
      //.tabBar('设备信息')
      .tabBar(this.MyTabBuilder(TabID.Device_information))

      TabContent(){
        //Text('太阳能')
        DriveComponent5()
      }
      //.tabBar('太阳能')
      .tabBar(this.MyTabBuilder(TabID.solar_energy))

      TabContent(){
        //Text('我的')
        DriveComponent3()
      }
      //.tabBar('我的')
      .tabBar(this.MyTabBuilder(TabID.MINE))


    }
    .barWidth('100%')
    .barMode(BarMode.Fixed)
    .width('100%')
    .height('100%')
    .onChange((index)=>{
      this.pageIndex = index;
    })

  }
}