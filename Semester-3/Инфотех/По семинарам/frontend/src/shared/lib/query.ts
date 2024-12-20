import {API_URL} from './config.ts'

type Method = 'get' | 'put' | 'post' | 'delete'

export const query = async (suffix: string, method: Method = 'get', data: any = {}, controller?: AbortController, headers?: Record<string, string>) => {

  const request_headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...headers
  }

  let request_data: BodyInit | null = method !== 'get' ? JSON.stringify(data) : null

  if (request_headers['Content-Type'] === 'multipart/form-data') {
    delete request_headers['Content-Type']
    request_data = data
  }

  const res = await fetch(API_URL + suffix, {
    method: method.toUpperCase(),
    credentials: 'include',
    headers: request_headers,
    body: request_data,
    signal: controller?.signal
  })

  const json = await res.json()

  if (json.error?.message) throw new ApiError(
    json.error.message,
    json.error.type,
    json.error.code,
    json.error.attachments
  )

  if (!res.ok) {

    if (json?.error) throw new ApiError(json.error)

    throw new ApiError('Не удалось подключиться к серверу')
  }

  return json.response ?? json
}

export class ApiError extends Error {

  type: string
  message: string
  code: number
  attachments: object

  constructor(message: string, type: string = 'execution', code: number = -1, attachments: object = {}) {
    super(message)
    this.message = message
    this.code = code
    this.type = type
    this.attachments = attachments
  }

}