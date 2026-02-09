import request from '@/utils/request'

// 请求配置
export interface ScanResult {
  document_id: string
  image_url: string
  ocr_result: {
    text: string
    texts: string[]
    positions: number[][][]
    count: number
  }
}

// OCR识别
export const ocrImage = async (file: File, lang: string = 'ch') => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('lang', lang)
  formData.append('user_id', 'default')

  return request.post<ScanResult>('/ocr', formData)
}

// 文档扫描
export const scanDocument = async (
  file: File,
  enhance: boolean = true,
  auto_crop: boolean = true
) => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('enhance', String(enhance))
  formData.append('auto_crop', String(auto_crop))
  formData.append('user_id', 'default')

  return request.post<ScanResult>('/scan', formData)
}

// 导出PDF
export const exportPDF = async (images: string[], filename: string = 'document.pdf') => {
  return request.post<{ pdf_url: string }>('/pdf/export', {
    images,
    filename,
    user_id: 'default'
  })
}

// 完整文档处理
export const processDocument = async (
  file: File,
  options: {
    enhance?: boolean
    auto_crop?: boolean
    ocr?: boolean
    export_pdf?: boolean
  } = {}
) => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('enhance', String(options.enhance ?? true))
  formData.append('auto_crop', String(options.auto_crop ?? true))
  formData.append('ocr', String(options.ocr ?? true))
  formData.append('export_pdf', String(options.export_pdf ?? true))
  formData.append('user_id', 'default')

  return request.post<ScanResult & { pdf_url?: string }>('/document/process', formData)
}

// 证件扫描
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
