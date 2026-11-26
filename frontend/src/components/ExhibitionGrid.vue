<script setup>
import { computed } from 'vue'
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

  switch (error.kind) {
    case 'network':
      return {
        title: '连不上后端服务',
        message:
          '请确认 API 已启动：在 backend 目录执行 uvicorn app.main:app --port 8000，然后重试。',
      }
    case 'timeout':
      return { title: '请求超时', message: '后端响应过慢，请稍后重试。' }
    case 'invalid':
      return { title: '筛选条件不合法', message: error.message || '请调整条件后重试。' }
    case 'parse':
      return { title: '返回数据无法解析', message: error.message || '请检查后端接口输出。' }
    default:
      return { title: '服务返回错误', message: error.message || '请稍后重试。' }
  }
})

const emptyView = computed(() => {
  if (props.hasFilters) {
    return {
      title: '没有符合条件的展会',
      message: '换个关键词，或切回「全部在展」看看。',
      actionLabel: '清除筛选',
      action: 'clear',
    }
  }
  return {
    title: '还没有采集到展会',
    message:
      '数据库里暂时没有未结束的展会。可以手动触发一次抓取：POST /api/exhibitions/crawl，完成后刷新本页。',
    actionLabel: '重新加载',
    action: 'retry',
  }
})
</script>

<template>
  <section class="list" aria-live="polite">
    <div v-if="!error" class="list__head">
      <h2 class="list__title">近期展会</h2>
      <p class="list__hint">按开幕时间由近到远</p>
    </div>

    <CardSkeleton v-if="showSkeleton" :count="Math.min(pageSize, 6)" />

    <StatePanel
      v-else-if="error"
      kind="error"
      :title="errorView.title"
      :message="errorView.message"
      action-label="重试"
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
