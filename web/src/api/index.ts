import request from '@/utils/request'

// 通用类型
export interface Document {
  id: string
  name: string
  type: string
  created_at: string | null
  status: string
  metadata?: any
}

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

// 获取文档列表
export const getDocuments = async (user_id: string = 'default') => {
  return request.get<Document[]>('/documents', {
    params: { user_id }
  })
}

// 获取文档详情
export interface DocumentDetail extends Document {
  text: string
  textCount: number
  image_url?: string
}

export const getDocument = async (document_id: string, user_id: string = 'default') => {
  return request.get<DocumentDetail>(`/documents/${document_id}`, {
    params: { user_id }
  })
}

// 删除文档
export const deleteDocument = async (document_id: string, user_id: string = 'default') => {
  return request.delete(`/documents/${document_id}`, {
    params: { user_id }
  })
}

// 获取扫描历史
export interface ScanHistoryItem {
  id: string
  name: string
  timestamp: string | null
  textCount: number
}

export const getScanHistory = async (user_id: string = 'default') => {
  return request.get<ScanHistoryItem[]>('/history', {
    params: { user_id }
  })
}
