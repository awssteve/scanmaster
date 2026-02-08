import { window } from '@kit.ArkUI';
import router from '@system.router';

@Entry
@Component
export struct ExportExcel {
  @State texts: string[] = [];
  @State loading: boolean = false;
  @State resultUrl: string = '';

  build() {
    Column() {
      Text('转Excel表格')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .margin({ bottom: 20 })

      Button('添加文字')
        .width('calc(100% - 40px)')
        .height(56)
        .fontSize(18)
        .margin({ left: 20, right: 20, bottom: 20 })
        .onClick(() => this.addText())

      if (this.texts.length > 0) {
        List({ space: 12 }) {
          ForEach(this.texts) {
            ListItem() {
              Text($item)
                .fontSize(16)
                .fontColor('#333333')
            }
            .padding(16)
            .borderRadius(8)
            .backgroundColor(Color.White)
            .swipeAction({ end: true }) {
              ListItemGroup() {
                ListItem()
                  .width('100%')
                  .onClick(() => {
                    this.deleteItem($item);
                  })
              }
            }
          }
          .width('calc(100% - 40px)')
          .margin({ left: 20 })
        }
        .margin({ bottom: 20 })
      }

      Button('导出Excel')
        .width('calc(100% - 40px)')
        .height(56)
        .fontSize(18)
        .margin({ left: 20, right: 20, bottom: 20 })
        .padding({ left: 20, right: 20 })
        .enabled(!this.loading && this.texts.length > 0)
        .onClick(() => this.handleExport())

      if (this.resultUrl) {
        Column() {
          Text('导出成功')
            .fontSize(18)
            .fontWeight(FontWeight.Bold)
            .margin({ top: 40, bottom: 20 })

          Text(`文件地址：${this.resultUrl}`)
            .fontSize(16)
            .fontColor('#666666')
            .margin({ bottom: 20 })

          Button('下载文件')
            .width('calc(100% - 40px)')
            .height(56)
            .margin({ left: 20, right: 20 })
            .onClick(() => this.handleDownload())
        }
        .padding({ left: 20, right: 20 })
      }

      if (this.loading) {
        Row() {
          Blank()
          LoadingProgress()
            .color('#409EFF')
            .width('100%')
        }
        .width('100%')
        .height(200)
        .margin({ top: 40 })
      }
    }
    .width('100%')
    .height('100%')
    .padding({ top: 20 })
    .backgroundColor('#F5F7FA')
  }

  addText() {
    // TODO: 弹出输入框
    const newText = `文字 ${this.texts.length + 1}`;
    this.texts.push(newText);
  }

  deleteItem(text: string) {
    const index = this.texts.indexOf(text);
    if (index > -1) {
      this.texts.splice(index, 1);
    }
  }

  async handleExport() {
    if (this.texts.length === 0) {
      return;
    }

    this.loading = true;

    try {
      // TODO: 调用后端导出Excel API
      // const result = await this.officeService.exportToExcel(this.texts);

      // 模拟结果
      await new Promise<void>(resolve => setTimeout(resolve, 1500));
      this.resultUrl = 'http://localhost/static/excel/table.xlsx';
    } catch (err) {
      console.error('Export Excel failed:', JSON.stringify(err));
    } finally {
      this.loading = false;
    }
  }

  handleDownload() {
    if (!this.resultUrl) return;

    // TODO: 下载文件
    console.log('Download file:', this.resultUrl);
  }
}
