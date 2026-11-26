<script setup>
import { computed } from 'vue'
import { t } from '../i18n'
import CardSkeleton from './CardSkeleton.vue'
import ExhibitionCard from './ExhibitionCard.vue'
import StatePanel from './StatePanel.vue'

const props = defineProps({
  items: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  error: { type: Object, default: null },
  hasFilters: { type: Boolean, default: false },
  pageSize: { type: Number, default: 12 },
})

const emit = defineEmits(['retry', 'clear'])

/** 首次加载或换筛选条件后没有任何数据时，才展示骨架屏 */
const showSkeleton = computed(() => props.loading && props.items.length === 0)
/** 已有数据、正在请求新数据：保留旧列表并弱化 */
const isStale = computed(() => props.loading && props.items.length > 0)

const errorView = computed(() => {
  const error = props.error
  if (!error) return null

  const known = ['network', 'timeout', 'invalid', 'parse'].includes(error.kind)
    ? error.kind
    : 'http'
  const useServerMessage = (known === 'invalid' || known === 'http') && error.message

  return {
    title: t(`error.${known}.title`),
    message: useServerMessage ? error.message : t(`error.${known}.message`),
  }
})

const emptyView = computed(() => {
  if (props.hasFilters) {
    return {
      title: t('empty.filtered.title'),
      message: t('empty.filtered.message'),
      actionLabel: t('action.clearFilters'),
      action: 'clear',
    }
  }
  return {
    title: t('empty.nodata.title'),
    message: t('empty.nodata.message'),
    actionLabel: t('action.reload'),
    action: 'retry',
  }
})
</script>

<template>
  <section class="list" aria-live="polite">
    <div v-if="!error" class="list__head">
      <h2 class="list__title">{{ t('list.title') }}</h2>
      <p class="list__hint">{{ t('list.hint') }}</p>
    </div>

    <CardSkeleton v-if="showSkeleton" :count="Math.min(pageSize, 6)" />

    <StatePanel
      v-else-if="error"
      kind="error"
      :title="errorView.title"
      :message="errorView.message"
      :action-label="t('action.retry')"
      @action="emit('retry')"
    />

    <StatePanel
      v-else-if="!items.length"
      kind="empty"
      :title="emptyView.title"
      :message="emptyView.message"
      :action-label="emptyView.actionLabel"
      @action="emit(emptyView.action)"
    />

    <div v-else class="list__grid" :class="{ 'list__grid--stale': isStale }">
      <ExhibitionCard v-for="item in items" :key="item.id" :item="item" />
    </div>
  </section>
</template>

<style scoped>
.list {
  position: relative;
}

.list__head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.list__title {
  font-size: 15px;
  font-weight: 640;
  letter-spacing: 0.01em;
}

.list__hint {
  font-size: 12.5px;
  color: var(--text-faint);
}

.list__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(430px, 1fr));
  gap: 14px;
  transition: opacity 0.18s ease;
}

.list__grid--stale {
  opacity: 0.5;
  pointer-events: none;
}

@media (max-width: 960px) {
  .list__grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .list__grid {
    gap: 10px;
  }
}
</style>
