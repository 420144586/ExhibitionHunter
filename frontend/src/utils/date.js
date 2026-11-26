/**
 * 日期展示、状态推导与倒计时。
 *
 * 后端返回的是「无时区的本地时间」字符串，例如 2026-12-05T00:00:00，
 * new Date() 在本地时区解析即可，不要再做时区换算。
 *
 * 与语言相关的部分（月份名、日期格式）按 locale 分支；
 * 纯文案（"今天开幕"等）由调用方用 i18n 的 key 渲染。
 */

const DAY_MS = 86400000

const MONTHS_SHORT = [
  'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
]

export function parseDate(value) {
  if (!value) return null
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? null : date
}

function startOfDay(date) {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate())
}

function endOfDay(date) {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate(), 23, 59, 59, 999)
}

/** UTC 归一化后的整日差，避免时区/夏令时误差 */
function dayDiff(from, to) {
  const a = Date.UTC(from.getFullYear(), from.getMonth(), from.getDate())
  const b = Date.UTC(to.getFullYear(), to.getMonth(), to.getDate())
  return Math.round((b - a) / DAY_MS)
}

function pad(n) {
  return String(n).padStart(2, '0')
}

function monthLabel(date, locale) {
  return locale === 'zh' ? `${date.getMonth() + 1}月` : MONTHS_SHORT[date.getMonth()]
}

/** 大号日期角标：中文 { month: '12月', day: '05' }，英文 { month: 'Dec', day: '05' } */
export function dateBadge(startValue, locale = 'zh') {
  const start = parseDate(startValue)
  if (!start) return { month: locale === 'zh' ? '待定' : 'TBD', day: '--' }
  return { month: monthLabel(start, locale), day: pad(start.getDate()) }
}

/** 完整日期，用于 title 提示 */
export function formatFullDate(value, locale = 'zh') {
  const date = parseDate(value)
  if (!date) return ''
  if (locale === 'zh') {
    return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
  }
  return `${MONTHS_SHORT[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`
}

/**
 * 展期文案。
 *   中文：同月 12月5日 – 7日 / 同年 12月5日 – 1月3日 / 跨年 2026年12月5日 – 2027年1月3日
 *   英文：同月 Dec 5 – 7 / 同年 Dec 5 – Jan 3 / 跨年 Dec 5, 2026 – Jan 3, 2027
 * 缺开始或结束只有单边文案；两边都缺时返回空串，由调用方渲染"展期待定"。
 */
export function formatRange(startValue, endValue, locale = 'zh') {
  const start = parseDate(startValue)
  const end = parseDate(endValue)

  if (!start && !end) return ''

  if (locale === 'zh') {
    if (!start) return `截止 ${formatFullDate(endValue, 'zh')}`
    if (!end) return `${start.getMonth() + 1}月${start.getDate()}日 起`
    const sameYear = start.getFullYear() === end.getFullYear()
    const sameMonth = sameYear && start.getMonth() === end.getMonth()
    if (sameMonth) return `${start.getMonth() + 1}月${start.getDate()}日 – ${end.getDate()}日`
    if (sameYear) {
      return `${start.getMonth() + 1}月${start.getDate()}日 – ${end.getMonth() + 1}月${end.getDate()}日`
    }
    return `${formatFullDate(startValue, 'zh')} – ${formatFullDate(endValue, 'zh')}`
  }

  if (!start) return `Until ${formatFullDate(endValue, 'en')}`
  if (!end) return `From ${formatFullDate(startValue, 'en')}`
  const sameYear = start.getFullYear() === end.getFullYear()
  const sameMonth = sameYear && start.getMonth() === end.getMonth()
  if (sameMonth) {
    return `${MONTHS_SHORT[start.getMonth()]} ${start.getDate()} – ${end.getDate()}`
  }
  if (sameYear) {
    return `${MONTHS_SHORT[start.getMonth()]} ${start.getDate()} – ${MONTHS_SHORT[end.getMonth()]} ${end.getDate()}`
  }
  return `${formatFullDate(startValue, 'en')} – ${formatFullDate(endValue, 'en')}`
}

/** 展期天数（含首尾）；缺日期返回 null */
export function durationDays(startValue, endValue) {
  const start = parseDate(startValue)
  const end = parseDate(endValue)
  if (!start || !end) return null
  return dayDiff(start, end) + 1
}

/**
 * 展示用状态：ongoing / upcoming / ended。
 * 与后端口径一致：开始时间晚于当前时刻即 upcoming；
 * 结束时间按当日 23:59:59 计，避免「当天结束」被显示成已结束。
 */
export function deriveStatus(startValue, endValue, now = new Date()) {
  const start = parseDate(startValue)
  const end = parseDate(endValue)
  if (start && start > now) return 'upcoming'
  if (end && endOfDay(end) < now) return 'ended'
  return 'ongoing'
}

/**
 * 倒计时的文案 key + 参数，交给 i18n 渲染。
 * 返回 null 表示不需要展示。
 */
export function countdownKey(startValue, endValue, now = new Date()) {
  const start = parseDate(startValue)
  const end = parseDate(endValue)

  if (start && start > now) {
    const days = dayDiff(startOfDay(now), startOfDay(start))
    if (days <= 0) return { key: 'countdown.opensToday' }
    if (days === 1) return { key: 'countdown.opensTomorrow' }
    return { key: 'countdown.opensInDays', params: { n: days } }
  }

  if (end) {
    const lastDay = endOfDay(end)
    if (lastDay > now) {
      const days = dayDiff(startOfDay(now), startOfDay(end))
      if (days <= 0) return { key: 'countdown.closesToday' }
      if (days === 1) return { key: 'countdown.closesTomorrow' }
      return { key: 'countdown.daysLeft', params: { n: days } }
    }
  }

  return null
}
