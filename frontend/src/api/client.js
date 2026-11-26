/**
 * 极简 fetch 封装：统一 baseURL、超时、错误归一化。
 *
 * 失败时抛出带 kind 的错误对象，页面只判断 kind：
 *   aborted  —— 调用方主动取消（不展示）
 *   timeout  —— 超时
 *   network  —— 连不上后端
 *   invalid  —— 参数不合法（HTTP 422）
 *   http     —— 其它 HTTP 错误
 *   parse    —— 响应不是合法 JSON
 */

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? ''
const DEFAULT_TIMEOUT = 15000

function toError(kind, message, extra = {}) {
  const error = new Error(message)
  error.kind = kind
  return Object.assign(error, extra)
}

/** 把 FastAPI 的 detail（字符串或字段级数组）压成一句可读文案 */
function readDetail(payload) {
  const detail = payload?.detail
  if (!detail) return ''
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        const field = Array.isArray(item?.loc) ? item.loc.filter((p) => p !== 'query').join('.') : ''
        return [field, item?.msg].filter(Boolean).join(': ')
      })
      .filter(Boolean)
      .join('；')
  }
  return String(detail)
}

export async function request(path, { signal, timeout = DEFAULT_TIMEOUT } = {}) {
  const controller = new AbortController()
  let timedOut = false
  let abortedByCaller = false

  const onCallerAbort = () => {
    abortedByCaller = true
    controller.abort()
  }

  if (signal) {
    if (signal.aborted) onCallerAbort()
    else signal.addEventListener('abort', onCallerAbort, { once: true })
  }

  const timer = setTimeout(() => {
    timedOut = true
    controller.abort()
  }, timeout)

  try {
    const response = await fetch(`${BASE_URL}${path}`, {
      method: 'GET',
      headers: { Accept: 'application/json' },
      signal: controller.signal,
    })

    if (!response.ok) {
      let detail = ''
      try {
        detail = readDetail(await response.json())
      } catch {
        // 响应体不是 JSON 时忽略，使用状态码兜底
      }
      const message = detail || `服务返回 ${response.status}`
      if (response.status === 422) throw toError('invalid', message, { status: 422 })
      throw toError('http', message, { status: response.status })
    }

    try {
      return await response.json()
    } catch {
      throw toError('parse', '响应内容不是合法的 JSON')
    }
  } catch (error) {
    if (error?.kind) throw error
    if (timedOut) throw toError('timeout', `请求超过 ${Math.round(timeout / 1000)} 秒未完成`)
    if (abortedByCaller) throw toError('aborted', '请求已取消')
    throw toError('network', '无法连接后端服务')
  } finally {
    clearTimeout(timer)
    if (signal) signal.removeEventListener('abort', onCallerAbort)
  }
}
