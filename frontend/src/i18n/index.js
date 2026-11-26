import { computed, ref, watch } from 'vue'
import { messages, SUPPORTED_LOCALES } from './messages'

const STORAGE_KEY = 'eh.locale'
const FALLBACK_LOCALE = 'zh'

function detectInitialLocale() {
  if (typeof window === 'undefined') return FALLBACK_LOCALE

  const saved = window.localStorage.getItem(STORAGE_KEY)
  if (saved && SUPPORTED_LOCALES.includes(saved)) return saved

  const preferred = (navigator.language || '').toLowerCase()
  return preferred.startsWith('zh') ? 'zh' : 'en'
}

function applyDocumentLanguage(value) {
  if (typeof document !== 'undefined') {
    document.documentElement.lang = value === 'zh' ? 'zh-CN' : 'en'
  }
}

export const locale = ref(detectInitialLocale())
export const isZh = computed(() => locale.value === 'zh')

/** 翻译；缺失的 key 依次回退：当前语言 → 中文 → key 本身 */
export function t(key, params) {
  const table = messages[locale.value] || messages[FALLBACK_LOCALE]
  let text = table[key]
  if (text === undefined) text = messages[FALLBACK_LOCALE][key]
  if (text === undefined) text = key

  if (params) {
    for (const [name, value] of Object.entries(params)) {
      text = text.split(`{${name}}`).join(String(value))
    }
  }
  return text
}

export function setLocale(next) {
  if (!SUPPORTED_LOCALES.includes(next) || next === locale.value) return
  locale.value = next
  if (typeof window !== 'undefined') window.localStorage.setItem(STORAGE_KEY, next)
}

export function toggleLocale() {
  setLocale(locale.value === 'zh' ? 'en' : 'zh')
}

// 语言变化时同步 <html lang> 与标签页标题
applyDocumentLanguage(locale.value)
if (typeof document !== 'undefined') {
  document.title = t('meta.title')
}

watch(locale, (value) => {
  applyDocumentLanguage(value)
  if (typeof document !== 'undefined') document.title = t('meta.title')
})
