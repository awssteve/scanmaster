import { window } from '@kit.ArkUI';
import router from '@system.router';

@Entry
@Component
export struct LongImage {
  @State imageUrls: string[] = [];
  @State spacing: number = 20;
  @State loading: boolean = false;
  @State resultUrl: string = '';

  build() {
    Column() {
      Text('创建长图片')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .margin({ bottom: 20 })

      // 图片选择
      Column() {
        Text('选择图片（{{ imageUrls.length }}/50）')
          .fontSize(16)
          .fontColor('#666666')
          .margin({ left: 20, right: 20, bottom: 12 })

        Grid({ columns: 4, rows: 3, gutter: 12 }) {
          ForEach(this.imageUrls) {
            GridCol() {
              Image($item)
                .width('100%')
                .aspectRatio(1)
                .objectFit(ImageFit.Cover)
                .borderRadius(8)
                .onClick(() => {
                  this.removeImage($item);
                })
            }
          }
        }
        .width('100%')
        .padding({ left: 20, right: 20 })
        .margin({ bottom: 20 })

        // 添加按钮
        if (this.imageUrls.length < 50) {
          Button('添加图片')
            .width('calc(100% - 40px)')
            .height(56)
            .margin({ left: 20, right: 20, bottom: 20 })
            .onClick(() => this.chooseImages())
        }
      }
      .width('100%')
      .padding({ left: 20, right: 20, top: 20 })

      // 间距设置
      if (this.imageUrls.length > 0) {
        Row() {
          Text('图片间距：')
            .fontSize(16)
            .fontColor('#666666')
            .width(100)
            .margin({ right: 16 })

          Slider({
            value: this.spacing,
            min: 0,
            max: 50,
            step: 5,
            style: SliderStyle.Outset
          })
            .width(300)
            .onChange((value: number) => {
              this.spacing = value;
            })
        }
        .width('100%')
        .padding({ left: 20, right: 20, top: 20, bottom: 20 })
        .alignItems(VerticalAlign.Center)
      }

      // 创建按钮
      if (this.imageUrls.length > 0) {
        Button('创建长图片')
          .width('calc(100% - 40px)')
          .height(56)
          .fontSize(18)
          .margin({ left: 20, right: 20, top: 20 })
          .padding({ left: 20, right: 20 })
          .enabled(!this.loading)
          .onClick(() => this.handleCreate())
      }

      // 结果展示
      if (this.resultUrl) {
        Column() {
          Text('创建成功')
            .fontSize(18)
            .fontWeight(FontWeight.Bold)
            .margin({ top: 40, bottom: 20 })

          Image(this.resultUrl)
            .width('100%')
            .height(400)
            .objectFit(ImageFit.Contain)
            .margin({ left: 20, right: 20, bottom: 20 })
            .borderRadius(12)

          Button('下载图片')
            .width('calc(100% - 40px)')
            .height(56)
            .margin({ left: 20, right: 20, top: 20 })
            .onClick(() => this.handleDownload())
        }
        .padding({ left: 20, right: 20, bottom: 20 })
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
    .backgroundColor('#F5F7FA')
  }

  async chooseImages() {
    if (this.imageUrls.length >= 50) {
      // 提示最多50张
      return;
    }

    // TODO: 调用图片选择器
    console.log('Choose images');
    // 模拟添加图片
    const newImage = '/common/images/placeholder.png';
    this.imageUrls.push(newImage);
  }

  removeImage(url: string) {
    const index = this.imageUrls.indexOf(url);
    if (index > -1) {
      this.imageUrls.splice(index, 1);
    }
  }

  async handleCreate() {
    if (this.imageUrls.length === 0) {
      return;
    }

    this.loading = true;

    try {
      // TODO: 调用后端创建长图片API
      // const result = await this.longImageService.createLongImage(this.imageUrls, this.spacing);

      // 模拟结果
      await new Promise<void>(resolve => setTimeout(resolve, 2000));
      this.resultUrl = 'http://localhost/static/images/long_image.png';
    } catch (err) {
      console.error('Create long image failed:', JSON.stringify(err));
    } finally {
      this.loading = false;
    }
  }

  handleDownload() {
    if (!this.resultUrl) return;

    // TODO: 下载图片
    console.log('Download image:', this.resultUrl);
  }
}
