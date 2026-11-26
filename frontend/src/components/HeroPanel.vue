<script setup>
import { ref, watch } from 'vue'
import { t } from '../i18n'

const props = defineProps({
  status: { type: String, default: 'all' },
  keyword: { type: String, default: '' },
})

const emit = defineEmits(['update:status', 'update:keyword'])

const STATUSES = [
  { value: 'all', key: 'tabs.all' },
  { value: 'ongoing', key: 'tabs.ongoing' },
  { value: 'upcoming', key: 'tabs.upcoming' },
]

const text = ref(props.keyword)

watch(
  () => props.keyword,
  (value) => {
    if (value !== text.value) text.value = value
  },
)

function onInput() {
  emit('update:keyword', text.value)
}

function onSubmit() {
  emit('update:keyword', text.value)
}

function clearInput() {
  text.value = ''
  emit('update:keyword', '')
}
</script>

<template>
  <section class="hero">
    <p class="hero__eyebrow">{{ t('hero.eyebrow') }}</p>

    <h1 class="hero__title">{{ t('hero.title') }}</h1>

    <p class="hero__lede">{{ t('hero.lede') }}</p>

    <form class="search" role="search" @submit.prevent="onSubmit">
      <svg class="search__icon" viewBox="0 0 20 20" aria-hidden="true">
        <circle cx="9" cy="9" r="6.2" fill="none" stroke="currentColor" stroke-width="1.8" />
        <path d="M13.6 13.6 17.4 17.4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
      </svg>

      <input
        v-model="text"
        class="search__input"
        type="search"
        name="keyword"
        :placeholder="t('hero.searchPlaceholder')"
        :aria-label="t('hero.searchLabel')"
        autocomplete="off"
        @input="onInput"
      />

      <button
        v-if="text"
        class="search__clear"
        type="button"
        :aria-label="t('hero.clearSearch')"
        @click="clearInput"
      >
        <svg viewBox="0 0 16 16" aria-hidden="true">
          <path
            d="M4 4l8 8M12 4l-8 8"
            stroke="currentColor"
            stroke-width="1.7"
            stroke-linecap="round"
          />
        </svg>
      </button>

      <button class="search__submit" type="submit">{{ t('hero.search') }}</button>
    </form>

    <div class="tabs" role="tablist" :aria-label="t('hero.statusLabel')">
      <button
        v-for="item in STATUSES"
        :key="item.value"
        class="tabs__tab"
        :class="{ 'tabs__tab--active': item.value === status }"
        type="button"
        role="tab"
        :aria-selected="item.value === status"
        @click="emit('update:status', item.value)"
      >
        {{ t(item.key) }}
      </button>
    </div>
  </section>
</template>

<style scoped>
.hero {
  padding: 56px 0 30px;
}

.hero__eyebrow {
  display: inline-block;
  padding: 4px 10px;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: var(--surface);
  color: var(--text-soft);
  font-size: 12px;
  letter-spacing: 0.06em;
}

.hero__title {
  margin: 18px 0 0;
  font-size: clamp(30px, 5.2vw, 46px);
  line-height: 1.14;
  font-weight: 680;
  letter-spacing: -0.02em;
  text-wrap: balance;
}

.hero__lede {
  margin-top: 14px;
  max-width: 52ch;
  color: var(--text-soft);
  font-size: 15px;
}

/* 搜索框 */
.search {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 26px;
  max-width: 620px;
  padding: 6px 6px 6px 14px;
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-lg);
  background: var(--surface);
  box-shadow: var(--shadow-sm);
  transition: border-color 0.18s ease, box-shadow 0.18s ease;
}

.search:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-soft);
}

.search__icon {
  flex: 0 0 auto;
  width: 19px;
  height: 19px;
  color: var(--text-faint);
}

.search__input {
  flex: 1 1 auto;
  min-width: 0;
  padding: 9px 2px;
  border: 0;
  background: transparent;
  font-size: 15px;
  outline: none;
}

.search__input::placeholder {
  color: var(--text-faint);
}

.search__input::-webkit-search-cancel-button {
  display: none;
}

.search__clear {
  flex: 0 0 auto;
  display: grid;
  place-items: center;
  width: 26px;
  height: 26px;
  border-radius: 999px;
  color: var(--text-faint);
}

.search__clear:hover {
  background: var(--surface-2);
  color: var(--text-soft);
}

.search__clear svg {
  width: 14px;
  height: 14px;
}

.search__submit {
  flex: 0 0 auto;
  padding: 9px 18px;
  border-radius: calc(var(--radius-lg) - 6px);
  background: var(--accent);
  color: var(--on-accent);
  font-size: 14px;
  font-weight: 600;
  transition: background 0.18s ease;
}

.search__submit:hover {
  background: var(--accent-hover);
}

/* 状态切换 */
.tabs {
  display: inline-flex;
  gap: 4px;
  margin-top: 22px;
  padding: 4px;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: var(--surface-2);
}

.tabs__tab {
  padding: 7px 16px;
  border-radius: 999px;
  color: var(--text-soft);
  font-size: 13.5px;
  font-weight: 550;
  transition: background 0.18s ease, color 0.18s ease;
  white-space: nowrap;
}

.tabs__tab:hover {
  color: var(--text);
}

.tabs__tab--active {
  background: var(--surface);
  color: var(--text);
  box-shadow: var(--shadow-sm);
}

@media (max-width: 640px) {
  .hero {
    padding: 34px 0 22px;
  }

  .search {
    flex-wrap: nowrap;
    padding-left: 11px;
  }

  .search__input {
    flex-basis: auto;
    font-size: 14.5px;
  }

  .search__submit {
    padding: 8px 15px;
    font-size: 13.5px;
  }

  .tabs {
    display: flex;
    width: 100%;
  }

  .tabs__tab {
    flex: 1 1 0;
    padding: 7px 8px;
    text-align: center;
  }
}
</style>
