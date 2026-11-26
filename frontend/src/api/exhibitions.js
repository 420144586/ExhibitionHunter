import { request } from './client'

/**
 * 展会列表。
 *
 * 与后端契约保持一致（见 doc/开发文档.md 4.4）：
 *   GET /api/exhibitions?page&page_size&status&city&industry&keyword
 *   返回 { items, total, page, page_size }
 *
 * @param {object} params
 * @param {number} [params.page=1]        页码，从 1 开始
 * @param {number} [params.page_size=12]  每页条数，后端上限 100
 * @param {'all'|'ongoing'|'upcoming'} [params.status='all']
 * @param {string} [params.keyword]       仅匹配展会名称
 * @param {AbortSignal} [signal]
 */
export function listExhibitions(params = {}, signal) {
  const search = new URLSearchParams()

  Object.entries(params).forEach(([key, value]) => {
    if (value === '' || value === null || value === undefined) return
    search.set(key, String(value))
  })

  const query = search.toString()
  return request(`/api/exhibitions${query ? `?${query}` : ''}`, { signal })
}
