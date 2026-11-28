<script setup>
import { computed } from 'vue'
import { locale, t } from '../i18n'
import { accentStyle } from '../utils/accent'
import {
  countdownKey,
  dateBadge,
  deriveStatus,
  durationDays,
  formatFullDate,
  formatRange,
} from '../utils/date'

const props = defineProps({
  item: { type: Object, required: true },
})

const badge = computed(() => dateBadge(props.item.start_date, locale.value))
const range = computed(() => formatRange(props.item.start_date, props.item.end_date, locale.value))
const status = computed(() => deriveStatus(props.item.start_date, props.item.end_date))
const statusLabel = computed(() => t(`status.${status.value}`))
const days = computed(() => durationDays(props.item.start_date, props.item.end_date))
const place = computed(() => [props.item.city, props.item.venue].filter(Boolean).join(' · '))
const tint = computed(() => accentStyle(props.item.title || props.item.source_id))

const countdown = computed(() => {
  const info = countdownKey(props.item.start_date, props.item.end_date)
  return info ? t(info.key, info.params) : ''
})

const rangeTitle = computed(() => {
  const parts = [
    formatFullDate(props.item.start_date, locale.value),
    formatFullDate(props.item.end_date, locale.value),
  ].filter(Boolean)
  return parts.length ? parts.join(' — ') : t('card.rangeTbd')
})
</script>

<template>
  <article class="card" :style="tint">
    <div class="card__aside">
      <p class="card__badge">
        <span class="card__month">{{ badge.month }}</span>
        <span class="card__day">{{ badge.day }}</span>
      </p>
      <span class="pill" :class="`pill--${status}`">{{ statusLabel }}</span>
    </div>

    <div class="card__body">
      <h3 class="card__title">{{ item.title }}</h3>

      <a
        v-if="item.source_url"
        class="card__url"
        :href="item.source_url"
        target="_blank"
        rel="noopener noreferrer"
        :title="item.source_url"
      >{{ item.source_url }}</a>

      <p class="card__place" :class="{ 'card__place--muted': !place }">
        {{ place || t('card.placeTbd') }}
      </p>

      <p class="card__range" :title="rangeTitle">
        <span>{{ range || t('card.rangeTbd') }}</span>
        <span v-if="days" class="card__days">{{ t('card.days', { n: days }) }}</span>
      </p>

      <p v-if="countdown" class="card__countdown">{{ countdown }}</p>
    </div>
  </article>
</template>

<style scoped>
.card {
  display: flex;
  gap: 16px;
  padding: 16px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  box-shadow: var(--shadow-sm);
  transition: border-color 0.18s ease, box-shadow 0.18s ease, transform 0.18s ease;
}

.card:hover {
  border-color: var(--border-strong);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

/* 左侧日期块：色相来自标题哈希，保证没有封面图也有辨识度 */
.card__aside {
  flex: 0 0 78px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.card__badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 12px 6px;
  border: 1px solid hsl(var(--card-hue) 42% 86%);
  border-radius: var(--radius-sm);
  background: hsl(var(--card-hue) 62% 96%);
  color: hsl(var(--card-hue) 52% 32%);
}

.card__month {
  font-size: 11.5px;
  font-weight: 600;
  letter-spacing: 0.04em;
  opacity: 0.85;
}

.card__day {
  margin-top: 1px;
  font-size: 25px;
  font-weight: 680;
  line-height: 1;
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.02em;
}

.card__body {
  flex: 1 1 auto;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.card__title {
  font-size: 16.5px;
  font-weight: 620;
  line-height: 1.42;
  letter-spacing: -0.01em;
  color: var(--text);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card__url {
  font-size: 12px;
  font-family: var(--mono);
  color: var(--accent);
  text-decoration: none;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card__url:hover {
  text-decoration: underline;
}

.card__place {
  font-size: 13.5px;
  color: var(--text-soft);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card__place--muted {
  color: var(--text-faint);
}

.card__range {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 7px;
  font-size: 13.5px;
  color: var(--text-soft);
  font-variant-numeric: tabular-nums;
}

.card__days {
  padding: 1px 7px;
  border-radius: 999px;
  background: var(--surface-2);
  color: var(--text-faint);
  font-size: 11.5px;
}

.card__countdown {
  margin-top: auto;
  padding-top: 2px;
  font-size: 12.5px;
  font-weight: 600;
  color: var(--accent);
}

@media (prefers-color-scheme: dark) {
  .card__badge {
    border-color: hsl(var(--card-hue) 24% 28%);
    background: hsl(var(--card-hue) 32% 17%);
    color: hsl(var(--card-hue) 62% 76%);
  }
}

@media (max-width: 420px) {
  .card__aside {
    flex-basis: 64px;
  }

  .card__day {
    font-size: 22px;
  }
}
</style>
