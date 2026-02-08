import { promptAction } from '@kit.ArkUI';
import router from '@system.router';

@Entry
@Component
export struct Watermark {
  @State imageUrl: string = '';
  @State activeTab: number = 0;
  @State watermarkType: string = 'text';
  @State watermarkText: string = '';
  @State watermarkPosition: string = 'bottom_right';
  @State watermarkOpacity: number = 0.3;
  @State processing: boolean = false;

  build() {
    Column() {
      Row() {
        Text('水印管理')
          .fontSize(20)
          .fontWeight(FontWeight.Bold)
        .margin({ right: 20 })

        Button('返回')
          .onClick(() => {
            router.back();
          })
      }
      .width('100%')
      .justifyContent(FlexAlign.SpaceBetween)
      .margin({ bottom: 20 })

      Tabs({ index: this.activeTab }) {
        TabContent() {
          Column({ space: 20 }) {
            Text('上传图片')
              .fontSize(18)
              .margin({ bottom: 16 })

            if (!this.imageUrl) {
              Column() {
                Image('/common/images/upload_placeholder.png')
                  .width(200)
                  .height(200)
                  .objectFit(ImageFit.Contain)
                  .margin({ bottom: 16 })

                Button('选择图片')
                  .width(120)
                  .height(48)
                  .onClick(() => this.selectImage())
              }
              .width('100%')
              .alignItems(HorizontalAlign.Center)
            }
          }
        }

        TabContent() {
          Column({ space: 20 }) {
            if (this.imageUrl) {
              Row() {
                Text('水印类型：')
                  .fontSize(16)
                  .margin({ right: 20 })

                Radio({ group: 'watermarkType' })
                  .value(this.watermarkType)
                  .onChange((value: boolean) => {
                    if (value) {
                      this.watermarkType = 'text';
                    }
                  })

                  Text('文字')

                Radio({ group: 'watermarkType' })
                  .value(this.watermarkType === 'logo')
                  .onChange((value: boolean) => {
                    if (value) {
                      this.watermarkType = 'logo';
                    }
                  })

                  Text('Logo')
              }
              .width('100%')

              if (this.watermarkType === 'text') {
                TextInput({ placeholder: '输入水印文字', text: this.watermarkText })
                  .width('100%')
                  .margin({ top: 16 })
                  .onChange((value: string) => {
                    this.watermarkText = value;
                  })
              }
            }
          }
        }
      }
      .margin({ bottom: 20 })

      if (this.imageUrl && this.activeTab === 0) {
        Row() {
          Button('开始去水印')
            .enabled(!this.processing)
            .onClick(() => this.handleRemoveWatermark())
        }
        .width('100%')
      }

      if (this.imageUrl && this.activeTab === 1) {
        Column({ space: 16 }) {
          TextInput({ placeholder: '水印文字', text: this.addWatermarkText })
            .width('100%')
            .onChange((value: string) => {
              this.watermarkText = value;
            })

          Row() {
            Text('位置：')
              .fontSize(16)
              .margin({ right: 20 })

            Select([
              SelectOption({ value: 'top_left', label: '左上' }),
              SelectOption({ value: 'top_right', label: '右上' }),
              SelectOption({ value: 'bottom_left', label: '左下' }),
              SelectOption({ value: 'bottom_right', label: '右下' }),
              SelectOption({ value: 'center', label: '居中' })
            ])
            .selected(this.watermarkPosition)
            .onSelect((index: number) => {
              const options = ['top_left', 'top_right', 'bottom_left', 'bottom_right', 'center'];
              this.watermarkPosition = options[index];
            })
          }
          .width('100%')
          .margin({ top: 16 })

          Text('透明度：')
            .fontSize(16)
            .margin({ top: 16, bottom: 8 })

          Slider({
            value: this.watermarkOpacity,
            min: 0,
            max: 1,
            step: 0.1,
            style: SliderStyle.Outset
          })
          .width('100%')
          .onChange((value: number) => {
            this.watermarkOpacity = value;
          })

          Button('添加水印')
            .enabled(!this.processing)
            .onClick(() => this.handleAddWatermark())
          .width('100%')
          .height(56)
          .margin({ top: 20 })
        }
      }

      if (this.processing) {
        Row() {
          Blank()
          LoadingProgress()
            .color('#409EFF')
            .width('100%')
          .height(40)
        }
        .width('100%')
        .margin({ top: 40 })
      }
    }
    .width('100%')
    .height('100%')
    .padding(20)
    .backgroundColor(Color.White)
    .borderRadius(16)
  }

  selectImage() {
    // TODO: 调用图片选择器
    console.log('Select image');
    this.imageUrl = '/common/images/placeholder.png';
  }

  async handleRemoveWatermark() {
    this.processing = true;

    try {
      // TODO: 调用后端去水印API
      await new Promise<void>(resolve => setTimeout(resolve, 2000));

      // 模拟结果
      console.log('Remove watermark completed');
    } catch (err) {
      console.error('Remove watermark failed:', JSON.stringify(err));
    } finally {
      this.processing = false;
    }
  }

  async handleAddWatermark() {
    this.processing = true;

    try {
      // TODO: 调用后端添加水印API
      await new Promise<void>(resolve => setTimeout(resolve, 2000));

      console.log('Add watermark completed');
    } catch (err) {
      console.error('Add watermark failed:', JSON.stringify(err));
    } finally {
      this.processing = false;
    }
  }
}
