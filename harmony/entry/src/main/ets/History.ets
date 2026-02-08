import router from '@system.router';

@Entry
@Component
export struct History {
  @State history: Array<HistoryItem> = [];

  async aboutToAppear() {
    this.loadHistory();
  }

  loadHistory() {
    // TODO: 从后端加载历史记录
    // 模拟数据
    this.history = [
      {
        id: '1',
        name: '证件扫描',
        timestamp: new Date().toISOString(),
        textCount: 10
      },
      {
        id: '2',
        name: '文档扫描',
        timestamp: new Date(Date.now() - 86400000).toISOString(),
        textCount: 20
      }
    ];
  }

  clearHistory() {
    console.log('Clear history');
    this.history = [];
  }

  viewHistory(item: HistoryItem) {
    console.log('View history item:', item.id);
    // router.pushUrl({
    //   url: `pages/HistoryResult/Index?id=${item.id}`
    // });
  }

  build() {
    Column() {
      Text('历史记录')
        .fontSize(20)
        .fontWeight(FontWeight.Bold)
        .margin({ left: 20, top: 20, bottom: 20 })

      ForEach(this.history) {
        ListItem() {
          Row() {
            Column() {
              Text($r('item.name'))
                .fontSize(18)
                .fontWeight(FontWeight.Medium)
                .margin({ bottom: 10 })

              Text(`识别文字数：${$r('item.textCount')}`)
                .fontSize(14)
                .fontColor('#666666')
            }
            .layoutWeight(1)

            Text(this.formatTime($r('item.timestamp')))
              .fontSize(14)
              .fontColor('#999999')

            Blank()
              .width(20)

            Text('>')
              .fontSize(20)
              .fontColor('#CCCCCC')
          }
          .padding({ left: 20, right: 20 })
          .margin({ bottom: 12 })
          .borderRadius(12)
          .backgroundColor(Color.White)
          .onClick(() => this.viewHistory($r('item')))
        }
      }

      Row() {
        Blank()

        Column() {
          Text('暂无历史记录')
            .fontSize(16)
            .fontColor('#999999')
            .margin({ top: 200 })

          Button('开始扫描')
            .width(120)
            .height(48)
            .fontSize(16)
            .backgroundColor('#409EFF')
            .fontColor(Color.White)
            .onClick(() => {
              router.pushUrl({
                url: 'pages/Scan/Index'
              })
            })
        }
        .width('100%')
        .height(300)
        .justifyContent(FlexAlign.Center)
        .margin({ top: 40 })
      }
    }
    .width('100%')
    .padding({ left: 20, right: 20, top: 20 })
    .backgroundColor('#f5f7fa')
  }

  formatTime(timestamp: string): string {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now.getTime() - date.getTime();

    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return '刚刚';
    if (minutes < 60) return `${minutes}分钟前`;
    if (hours < 24) return `${hours}小时前`;
    return `${days}天前`;
  }
}

interface HistoryItem {
  id: string
  name: string
  timestamp: string
  textCount: number
}
