import { ocrImage, scanDocument, exportPDF, processDocument } from '@/api'

export interface IDCardResult {
  document_id: string
  card_type: string
  image_url: string
  ocr_result: {
    text: string
    texts: string[]
    positions: number[][][]
    count: number
  }
  id_info: {
    name?: string
    id_number?: string
    address?: string
    phone?: string
    issue_date?: string
    expiry_date?: string
  }
}

// 证件扫描
export const scanIdCard = async (
  file: File,
  card_type: string = 'id_card',
  enhance: boolean = true,
  auto_crop: boolean = true
) => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('card_type', card_type)
  formData.append('enhance', String(enhance))
  formData.append('auto_crop', String(auto_crop))
  formData.append('user_id', 'default')

  return request.post<IDCardResult>('/id-card/scan', formData)
}

export {
  ocrImage,
  scanDocument,
  exportPDF,
  processDocument
}
