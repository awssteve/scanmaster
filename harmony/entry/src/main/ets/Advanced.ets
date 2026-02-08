import router from '@system.router';

@Entry
@Component
export struct Advanced {
  @State currentIndex: number = 0;
  @State categories: Array<Category> = [];

  aboutToAppear() {
    this.categories = [
      { id: 0, title: '去水印', desc: '智能去除图片中的水印', icon: '/common/images/remove_watermark.png' },
      { id: 1, title: '翻译', desc: 'OCR识别后自动翻译', icon: '/common/images/translate.png' },
      { id: 2, title: '文档转换', desc: '导出为Word/Excel文档', icon: '/common/images/convert.png' },
      { id: 3, title: '图片合成', desc: '长图片/网格图片合成', icon: '/common/images/merge.png' }
    ];
  }

  goToCategory(index: number) {
    switch (index) {
      case 0:
        router.pushUrl({ url: 'pages/Watermark/Index' });
        break;
      case 1:
        router.pushUrl({ url: 'pages/Translate/Index' });
        break;
      case 2:
        router.pushUrl({ url: 'pages/Convert/Index' });
        break;
      case 3:
        router.pushUrl({ url: 'pages/Merge/Index' });
        break;
      default:
        console.log('Invalid category index:', index);
    }
  }

  build() {
    Column({ space: 16 }) {
      Text('高级功能')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .margin({ top: 20, bottom: 20 })

      Grid({ columns: 2, rows: 2, gutter: 16 }) {
        ForEach(this.categories) {
          GridCol() {
            Column({ space: 12 }) {
              Image($r('item.icon'))
                .width(64)
                .height(64)
                .objectFit(ImageFit.Cover)

              Text($r('item.title'))
                .fontSize(18)
                .fontWeight(FontWeight.Medium)
                .margin({ bottom: 8 })

              Text($r('item.desc'))
                .fontSize(14)
                .fontColor('#666666')
            }
            .width('100%')
            .padding(24)
            .borderRadius(16)
            .backgroundColor(Color.White)
            .onClick(() => this.goToCategory($r('item.id')))
          }
        }
      }
    }
    .width('100%')
    .height('100%')
    .padding({ left: 20, right: 20, top: 20 })
    .backgroundColor('#F5F7FA')
  }
}

interface Category {
  id: number
  title: string
  desc: string
  icon: string
}
