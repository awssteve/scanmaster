import { window } from '@kit.ArkUI';
import router from '@system.router';

@Entry
@Component
export struct ExportWord {
  @State text: string = '';
  @State loading: boolean = false;
  @State resultUrl: string = '';

  build() {
    Column() {
      Text('转Word文档')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .margin({ bottom: 20 })

      Text('输入或粘贴要转换的文字：')
        .fontSize(16)
        .fontColor('#666666')
        .margin({ left: 20, right: 20, bottom: 12 })

      TextArea({ placeholder: '请输入文字...', text: this.text })
        .width('100%')
        .height(200)
        .margin({ left: 20, right: 20 })
        .onChange((value: string) => {
          this.text = value;
        })

      Button('导出Word')
        .width('calc(100% - 40px)')
        .height(56)
        .fontSize(18)
        .margin({ top: 20 })
        .padding({ left: 20, right: 20 })
        .enabled(!this.loading && this.text.length > 0)
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

  async handleExport() {
    if (!this.text) {
      return;
    }

    this.loading = true;

    try {
      // TODO: 调用后端导出Word API
      // const result = await this.officeService.exportToWord(this.text);

      // 模拟结果
      await new Promise<void>(resolve => setTimeout(resolve, 1500));
      this.resultUrl = 'http://localhost/static/word/document.docx';
    } catch (err) {
      console.error('Export Word failed:', JSON.stringify(err));
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
