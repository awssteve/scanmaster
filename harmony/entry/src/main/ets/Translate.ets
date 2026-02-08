import { window } from '@kit.ArkUI';
import router from '@system.router';

@Entry
@Component
export struct Translate {
  @State imageUrl: string = '';
  @State originalText: string = '';
  @State translatedText: string = '';
  @State fromLang: string = 'zh';
  @State toLang: string = 'en';
  @State loading: boolean = false;

  build() {
    Column() {
      Text('拍照翻译')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .margin({ bottom: 20 })

      // 图片上传
      Column() {
        if (this.imageUrl) {
          Image(this.imageUrl)
            .width('100%')
            .height(300)
            .objectFit(ImageFit.Cover)
            .margin({ top: 20 })
            .borderRadius(12)
            .onClick(() => this.chooseImage())
        } else {
          Column() {
            Image('/common/images/placeholder.png')
              .width('100%')
              .height(300)
              .objectFit(ImageFit.Cover)
              .margin({ top: 20 })
              .borderRadius(12)

            Text('点击图片开始翻译')
              .fontSize(16)
              .fontColor('#999999')
              .margin({ top: 20 })
          }
          .width('100%')
          .onClick(() => this.chooseImage())
        }
      }
      .width('100%')
      .padding({ left: 20, right: 20 })

      // 语言选择
      if (this.imageUrl) {
        Row({ space: 16 }) {
          Text('源语言：')
            .fontSize(16)
            .fontColor('#666666')
            .width(80)

          Select([
            SelectOption({ value: 'zh' }),
            SelectOption({ value: 'en' }),
            SelectOption({ value: 'ja' }),
            SelectOption({ value: 'ko' }),
            SelectOption({ value: 'fr' })
          ])
            .selected(this.fromLang)
            .onSelect((index: number) => {
              const options = ['zh', 'en', 'ja', 'ko', 'fr'];
              this.fromLang = options[index];
            })

          Blank()

          Text('目标语言：')
            .fontSize(16)
            .fontColor('#666666')
            .width(80)

          Select([
            SelectOption({ value: 'zh' }),
            SelectOption({ value: 'en' }),
            SelectOption({ value: 'ja' }),
            SelectOption({ value: 'ko' }),
            SelectOption({ value: 'fr' })
          ])
            .selected(this.toLang)
            .onSelect((index: number) => {
              const options = ['zh', 'en', 'ja', 'ko', 'fr'];
              this.toLang = options[index];
            })
        }
        .width('100%')
        .margin({ top: 20 })
        .padding({ left: 20, right: 20 })
      }

      // 翻译按钮
      if (this.imageUrl) {
        Button('开始翻译')
          .width('100%')
          .height(56)
          .fontSize(18)
          .margin({ top: 20 })
          .padding({ left: 20, right: 20 })
          .enabled(!this.loading)
          .onClick(() => this.handleTranslate())
      }

      // 结果展示
      if (this.translatedText) {
        Column() {
          Text('OCR识别结果')
            .fontSize(18)
            .fontWeight(FontWeight.Bold)
            .margin({ top: 40, bottom: 20 })

          Text(this.originalText)
            .fontSize(16)
            .fontColor('#333333')
            .padding({ left: 20, right: 20, top: 20, bottom: 20 })
            .backgroundColor('#F5F7FA')
            .borderRadius(10)
            .maxLines(10)
            .textOverflow({ overflow: TextOverflow.Ellipsis })

          Text('翻译结果')
            .fontSize(18)
            .fontWeight(FontWeight.Bold)
            .margin({ top: 20, bottom: 20 })

          Text(this.translatedText)
            .fontSize(16)
            .fontColor('#333333')
            .padding({ left: 20, right: 20, top: 20, bottom: 20 })
            .backgroundColor('#F0F9FF')
            .borderLeft({ width: 4, color: '#409EFF' })
            .maxLines(10)
            .textOverflow({ overflow: TextOverflow.Ellipsis })

          Row({ space: 16 }) {
            Button('复制原文')
              .onClick(() => this.handleCopyOriginal())

            Blank()

            Button('复制译文')
              .onClick(() => this.handleCopyTranslated())

            Blank()

            Button('导出Word')
              .onClick(() => this.handleExportWord())
          }
          .width('100%')
          .padding({ left: 20, right: 20, top: 20 })
          .justifyContent(FlexAlign.Center)
        }
        .padding({ left: 20, right: 20 })
      }

      // 加载状态
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

  chooseImage() {
    // TODO: 调用图片选择器
    console.log('Choose image for translation');
    this.imageUrl = '/common/images/placeholder.png';
  }

  async handleTranslate() {
    this.loading = true;

    try {
      // TODO: 调用翻译OCR API
      // const result = await this.translationService.translateOCR(this.imageUrl, this.fromLang, this.toLang);

      // 模拟结果
      this.originalText = '模拟OCR识别结果';
      this.translatedText = `模拟翻译结果 (${this.fromLang} -> ${this.toLang})`;
    } catch (err) {
      console.error('Translate failed:', JSON.stringify(err));
    } finally {
      this.loading = false;
    }
  }

  handleCopyOriginal() {
    if (!this.originalText) return;

    // TODO: 调用剪贴板API
    console.log('Copy original text:', this.originalText);
  }

  handleCopyTranslated() {
    if (!this.translatedText) return;

    // TODO: 调用剪贴板API
    console.log('Copy translated text:', this.translatedText);
  }

  handleExportWord() {
    // TODO: 调用导出Word API
    console.log('Export to Word');
  }
}
