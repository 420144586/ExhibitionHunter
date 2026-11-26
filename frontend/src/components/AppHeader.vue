<script setup>
import { t } from '../i18n'
import LanguageSwitcher from './LanguageSwitcher.vue'

defineProps({
  total: { type: Number, default: 0 },
  loading: { type: Boolean, default: false },
})
</script>

<template>
  <header class="site-header">
    <div class="container site-header__inner">
      <a class="brand" href="/" aria-label="ExhibitionHunter">
        <span class="brand__mark" aria-hidden="true">
          <svg viewBox="0 0 32 32" width="32" height="32">
            <rect width="32" height="32" rx="8" fill="currentColor" />
            <path
              d="M8.8 23.2V11.6L16 7.2l7.2 4.4v11.6"
              fill="none"
              stroke="#fff"
              stroke-width="2.2"
              stroke-linejoin="round"
            />
            <path
              d="M13.1 23.2v-6.1h5.8v6.1"
              fill="none"
              stroke="#fff"
              stroke-width="2.2"
              stroke-linejoin="round"
            />
          </svg>
        </span>
        <span class="brand__text">
          <strong>展会猎人</strong>
          <small>{{ t('header.brandSub') }}</small>
        </span>
      </a>

      <div class="site-header__right">
        <p class="site-header__stat">
          <template v-if="loading">
            <span class="site-header__dot" aria-hidden="true"></span>
            {{ t('header.syncing') }}
          </template>
          <template v-else-if="total > 0">
            {{ t('header.count', { n: total }) }}
          </template>
          <template v-else>{{ t('header.hint') }}</template>
        </p>
        <LanguageSwitcher />
      </div>
    </div>
  </header>
</template>

<style scoped>
.site-header {
  position: sticky;
  top: 0;
  z-index: 10;
  border-bottom: 1px solid var(--border);
  background: var(--bg);
  background: color-mix(in srgb, var(--bg) 88%, transparent);
  backdrop-filter: blur(12px);
}

.site-header__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  height: 66px;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: var(--text);
}

.brand__mark {
  color: var(--accent);
  display: block;
}

.brand__text {
  display: flex;
  flex-direction: column;
  line-height: 1.15;
}

.brand__text strong {
  font-size: 16px;
  font-weight: 650;
  letter-spacing: 0.02em;
  white-space: nowrap;
}

.brand__text small {
  font-size: 11px;
  color: var(--text-faint);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.site-header__right {
  display: flex;
  align-items: center;
  gap: 14px;
  min-width: 0;
}

.site-header__stat {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  font-size: 13px;
  color: var(--text-soft);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.site-header__dot {
  width: 7px;
  height: 7px;
  border-radius: 999px;
  background: var(--accent);
  animation: pulse 1.4s ease-in-out infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 0.35;
    transform: scale(0.85);
  }
  50% {
    opacity: 1;
    transform: scale(1);
  }
}

@media (max-width: 720px) {
  .site-header__stat {
    display: none;
  }
}

@media (max-width: 560px) {
  .brand__text small {
    display: none;
  }
}
</style>
