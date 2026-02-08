import router from '@system.router';
import { http } from '@kit.NetworkKit';

@Entry
@Component
export struct Documents {
  @State documents: Array<DocumentItem> = [];
  @State loading: boolean = false;

  async aboutToAppear() {
    await this.loadDocuments();
  }

  async loadDocuments() {
    this.loading = true;

    try {
      // TODO: 从后端获取文档列表
      // const result = await this.documentService.getDocuments();
      // this.documents = result.data;

      // 模拟数据
      this.documents = [
        {
          id: '1',
          name: '文档1.jpg',
          type: 'scan',
          created_at: new Date().toISOString()
        }
      ];
    } catch (err) {
      console.error('Load documents failed:', JSON.stringify(err));
    } finally {
      this.loading = false;
    }
  }

  async handleDelete(docId: string) {
    console.log('Delete document:', docId);

    try {
      // TODO: 调用后端删除文档
      // await this.documentService.deleteDocument(docId);

      // 从列表中移除
      this.documents = this.documents.filter((doc) => doc.id !== docId);
    } catch (err) {
      console.error('Delete document failed:', JSON.stringify(err));
    }
  }

  build() {
    Column() {
      Row() {
        Text('我的文档')
          .fontSize(20)
          .fontWeight(FontWeight.Bold)
          .margin({ left: 20 })

        Blank()

        Button('新建')
          .onClick(() => {
            router.pushUrl({
              url: 'pages/Scan/Index'
            })
          })
      }
      .width('100%')
      .padding({ left: 20, right: 20, top: 20 })
      .margin({ bottom: 20 })

      if (this.loading) {
        LoadingProgress()
          .color('#409EFF')
          .width('100%')
          .height(200)
      }

      ForEach(this.documents) {
        ListItem() {
          Row() {
            Image('/common/images/doc.png')
              .width(60)
              .height(60)
              .objectFit(ImageFit.Cover)
              .borderRadius(8)
              .margin({ right: 20 })

            Column() {
              Text($r('doc.name'))
                .fontSize(18)
                .fontWeight(FontWeight.Medium)
                .margin({ bottom: 8 })

              Text($r('doc.type'))
                .fontSize(14)
                .fontColor('#999999')
                .margin({ bottom: 6 })

              Text(this.formatTime($r('doc.created_at')))
                .fontSize(14)
                .fontColor('#999999')
            }
            .layoutWeight(1)
            .alignItems(HorizontalAlign.Center)

            Button('删除')
              .fontSize(14)
              .fontColor('#F56C6C')
              .onClick(() => this.handleDelete($r('doc.id')))
          }
          .padding({ left: 20, right: 20 })
          .margin({ bottom: 12 })
          .borderRadius(12)
          .backgroundColor(Color.White)
        }
      }
    }
    .width('100%')
    .padding({ left: 20, right: 20 })
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

interface DocumentItem {
  id: string
  name: string
  type: string
  created_at: string
}
