/**
 * 日期展示与状态推导。
 *
 * 后端返回的是「无时区的本地时间」字符串，例如 2026-12-05T00:00:00，
 * new Date() 在本地时区解析即可，不要再做时区换算。
 */

const DAY_MS = 86400000

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

/** 大号日期角标：{ month: '12月', day: '05' } */
export function dateBadge(startValue) {
  const start = parseDate(startValue)
  if (!start) return { month: '待定', day: '--' }
  return { month: `${start.getMonth() + 1}月`, day: pad(start.getDate()) }
}

/** 完整日期，用于 title 提示 */
export function formatFullDate(value) {
  const date = parseDate(value)
  if (!date) return ''
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
}

/**
 * 展期文案：
 *   同月   12月5日 – 7日
 *   同年   12月5日 – 1月3日
 *   跨年   2026年12月5日 – 2027年1月3日
 *   仅开始 12月5日 起
 */
export function formatRange(startValue, endValue) {
  const start = parseDate(startValue)
  const end = parseDate(endValue)

  if (!start && !end) return '展期待定'
  if (!start) return `截止 ${formatFullDate(endValue)}`
  if (!end) return `${start.getMonth() + 1}月${start.getDate()}日 起`

  const sameYear = start.getFullYear() === end.getFullYear()
  const sameMonth = sameYear && start.getMonth() === end.getMonth()

  if (sameMonth) return `${start.getMonth() + 1}月${start.getDate()}日 – ${end.getDate()}日`
  if (sameYear) {
    return `${start.getMonth() + 1}月${start.getDate()}日 – ${end.getMonth() + 1}月${end.getDate()}日`
  }
  return `${formatFullDate(startValue)} – ${formatFullDate(endValue)}`
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

export const STATUS_LABEL = {
  ongoing: '展出中',
  upcoming: '即将开始',
  ended: '已结束',
}

/** 「3 天后开幕」「还有 2 天」「今天闭幕」之类的相对提示 */
export function countdownText(startValue, endValue, now = new Date()) {
  const start = parseDate(startValue)
  const end = parseDate(endValue)

  if (start && start > now) {
    const days = dayDiff(startOfDay(now), startOfDay(start))
    if (days <= 0) return '今天开幕'
    if (days === 1) return '明天开幕'
    return `${days} 天后开幕`
  }

  if (end) {
    const lastDay = endOfDay(end)
    if (lastDay > now) {
      const days = dayDiff(startOfDay(now), startOfDay(end))
      if (days <= 0) return '今天闭幕'
      if (days === 1) return '明天闭幕'
      return `还有 ${days} 天`
    }
  }

  return ''
}
