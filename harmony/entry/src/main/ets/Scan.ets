import router from '@system.router';

@Entry
@Component
export struct Scan {
  @State imageUrl: string = '';
  @State ocrText: string = '';
  @State scanning: boolean = false;
  @State devicePosition: string = 'back';

  aboutToAppear() {
    // 初始化相机
    console.log('Scan page appeared');
  }

  async takePhoto() {
    // 调用相机拍照
    // 这里简化处理，实际需要集成相机模块
    console.log('Take photo, position:', this.devicePosition);
    this.scanning = true;

    try {
      // 模拟拍照延迟
      await new Promise<void>(resolve => setTimeout(resolve, 1000));

      // 模拟图片URL（实际应该是拍照后的路径）
      this.imageUrl = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect width="100" height="100" fill="%23409EFF"/></svg>';

      this.scanning = false;
    } catch (err) {
      console.error('Take photo failed:', JSON.stringify(err));
      this.scanning = false;
    }
  }

  toggleCamera() {
    this.devicePosition = this.devicePosition === 'back' ? 'front' : 'back';
    console.log('Camera position changed to:', this.devicePosition);
  }

  build() {
    Column() {
      // 顶部工具栏
      Row() {
        Button('翻转')
          .onClick(() => this.toggleCamera())

        Blank()
          .width(20)

        Button('闪光灯')
          .onClick(() => {
            console.log('Toggle flash');
          })
      }
      .width('100%')
      .height(60)
      .justifyContent(FlexAlign.SpaceAround)
      .padding({ left: 20, right: 20, top: 20 })

      // 预览区域
      Column() {
        if (this.imageUrl) {
          Image(this.imageUrl)
            .width('100%')
            .height(500)
            .objectFit(ImageFit.Cover)
            .margin({ top: 20 })
        } else {
          Column() {
            Text('相机预览')
              .fontSize(24)
              .fontColor('#999999')
              .margin({ top: 200 })
          }
          .width('100%')
          .height(500)
          .justifyContent(FlexAlign.Center)
          .backgroundColor('#f5f7fa')
          .margin({ top: 20 })
        }

        if (this.scanning) {
          LoadingProgress()
            .color('#409EFF')
            .width('100%')
            .height(40)
            .margin({ top: 40 })
        }
      }
      .width('100%')
      .layoutWeight(1)

      // 底部操作栏
      Row() {
        Button('取消')
          .onClick(() => {
            router.back();
          })

        Blank()
          .width(40)

        Button('拍照')
          .type(ButtonType.Capsule)
          .backgroundColor('#409EFF')
          .fontColor(Color.White)
          .width(120)
          .height(120)
          .onClick(() => this.takePhoto())
          .enabled(!this.scanning)

        Blank()
          .width(40)

        Button('相册')
          .onClick(() => {
            console.log('Open album');
          })
      }
      .width('100%')
      .height(160)
      .justifyContent(FlexAlign.SpaceAround)
      .margin({ top: 40 })
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#f5f7fa')
    .padding({ top: 20 })
  }
}
