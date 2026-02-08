import router from '@system.router';
import abilityAccessCtrl, Permissions, abilityAccessCtrl, createAtManager from '@ohos.abilityAccessCtrl';

@Entry
@Component
export struct Index {
  @State imageUrl: string = '';
  @State ocrText: string = '';
  @State loading: boolean = false;

  async aboutToAppear() {
    // 请求相机权限
    await this.requestCameraPermission();
  }

  async requestCameraPermission() {
    try {
      const atManager = abilityAccessCtrl.createAtManager();
      const permissions: Permissions = ['ohos.permission.CAMERA'];

      const grantStatus = await atManager.requestPermissionsFromUser(permissions, this.context);

      console.log('Camera permission:', JSON.stringify(grantStatus));
    } catch (err) {
      console.error('Request camera permission failed:', JSON.stringify(err));
    }
  }

  takePhoto() {
    // 调用相机拍照
    // 这里简化处理，实际需要集成相机模块
    console.log('Take photo');
  }

  async handleOCR() {
    if (!this.imageUrl) {
      console.log('No image selected');
      return;
    }

    this.loading = true;

    try {
      // TODO: 调用后端OCR API
      // const result = await this.ocrService.scanImage(this.imageUrl);

      // 模拟结果
      this.ocrText = '模拟OCR识别结果';
    } catch (err) {
      console.error('OCR failed:', JSON.stringify(err));
    } finally {
      this.loading = false;
    }
  }

  build() {
    Column() {
      Text('智扫通')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .margin({ bottom: 20 })

      Button('拍照扫描')
        .width('100%')
        .height(60)
        .fontSize(18)
        .onClick(() => this.takePhoto())

      if (this.imageUrl) {
        Image(this.imageUrl)
          .width('100%')
          .height(300)
          .objectFit(ImageFit.Cover)
          .margin({ top: 20 })
      }

      Button('开始识别')
        .width('100%')
        .height(60)
        .fontSize(18)
        .margin({ top: 20 })
        .enabled(!this.loading)
        .onClick(() => this.handleOCR())

      if (this.ocrText) {
        Text(this.ocrText)
          .width('100%')
          .fontSize(16)
          .margin({ top: 20 })
          .padding(20)
          .backgroundColor('#f5f7fa')
          .borderRadius(10)
      }

      if (this.loading) {
        LoadingProgress()
          .color('#409EFF')
          .width('100%')
          .height(40)
          .margin({ top: 20 })
      }
    }
    .width('100%')
    .height('100%')
    .padding(20)
    .backgroundColor('#f5f7fa')
  }
}
