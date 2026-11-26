import { computed, onUnmounted, reactive, ref } from 'vue'
import { listExhibitions } from '../api/exhibitions'

export const PAGE_SIZE_OPTIONS = [12, 24, 48]
const KEYWORD_DEBOUNCE = 320

/**
 * 展会列表的数据与交互状态。
 *
 * 负责：查询参数、请求取消、防抖、分页边界、错误归一化。
 * 不负责：任何 DOM 或样式。
 */
export function useExhibitionList() {
  const query = reactive({
    page: 1,
    page_size: PAGE_SIZE_OPTIONS[0],
    status: 'all',
    keyword: '',
  })

  const items = ref([])
  const total = ref(0)
  const loading = ref(false)
  const error = ref(null)

  let controller = null
  let requestSeq = 0
  let debounceTimer = null

  const pageCount = computed(() => Math.max(1, Math.ceil(total.value / query.page_size)))
  const hasFilters = computed(() => query.status !== 'all' || query.keyword.trim() !== '')

  async function load() {
    const seq = (requestSeq += 1)
    if (controller) controller.abort()
    controller = new AbortController()

    loading.value = true
    error.value = null

    try {
      const data = await listExhibitions({ ...query }, controller.signal)
      if (seq !== requestSeq) return
      items.value = Array.isArray(data?.items) ? data.items : []
      total.value = Number(data?.total ?? 0)
    } catch (err) {
      if (seq !== requestSeq) return
      if (err?.kind === 'aborted') return
      error.value = err
      items.value = []
      total.value = 0
    } finally {
      if (seq === requestSeq) loading.value = false
    }
  }

  function clearDebounce() {
    if (debounceTimer) {
      clearTimeout(debounceTimer)
      debounceTimer = null
    }
  }

  function loadFirstPage() {
    query.page = 1
    return load()
  }

  function setStatus(status) {
    if (query.status === status) return
    query.status = status
    clearDebounce()
    loadFirstPage()
  }

  /** 输入过程中调用：防抖后才真正请求 */
  function setKeyword(keyword) {
    query.keyword = keyword
    clearDebounce()
    debounceTimer = setTimeout(() => {
      debounceTimer = null
      loadFirstPage()
    }, KEYWORD_DEBOUNCE)
  }

  /** 回车/点搜索：立刻请求 */
  function submitKeyword(keyword) {
    query.keyword = keyword
    clearDebounce()
    loadFirstPage()
  }

  function setPage(page) {
    const next = Math.min(Math.max(1, page), pageCount.value)
    if (next === query.page) return
    query.page = next
    load()
    if (typeof window !== 'undefined') {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }

  function setPageSize(size) {
    if (query.page_size === size) return
    query.page_size = size
    loadFirstPage()
  }

  function clearFilters() {
    query.status = 'all'
    query.keyword = ''
    clearDebounce()
    loadFirstPage()
  }

  function retry() {
    load()
  }

  onUnmounted(() => {
    clearDebounce()
    if (controller) controller.abort()
  })

  load()

  return {
    query,
    items,
    total,
    loading,
    error,
    pageCount,
    hasFilters,
    setStatus,
    setKeyword,
    submitKeyword,
    setPage,
    setPageSize,
    clearFilters,
    retry,
  }
}
