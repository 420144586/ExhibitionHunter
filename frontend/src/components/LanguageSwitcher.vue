<script setup>
import { locale, setLocale, t } from '../i18n'

const OPTIONS = [
  { value: 'zh', label: '中文' },
  { value: 'en', label: 'EN' },
]
</script>

<template>
  <div class="lang" role="group" :aria-label="t('header.langLabel')">
    <button
      v-for="option in OPTIONS"
      :key="option.value"
      class="lang__btn"
      :class="{ 'lang__btn--active': locale === option.value }"
      type="button"
      :aria-pressed="locale === option.value"
      @click="setLocale(option.value)"
    >
      {{ option.label }}
    </button>
  </div>
</template>

<style scoped>
.lang {
  display: inline-flex;
  gap: 2px;
  padding: 3px;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: var(--surface-2);
}

.lang__btn {
  padding: 3px 9px;
  border-radius: 999px;
  color: var(--text-faint);
  font-size: 12px;
  font-weight: 600;
  line-height: 1.5;
  transition: background 0.18s ease, color 0.18s ease;
}

.lang__btn:hover {
  color: var(--text-soft);
}

.lang__btn--active {
  background: var(--surface);
  color: var(--text);
  box-shadow: var(--shadow-sm);
}
</style>
