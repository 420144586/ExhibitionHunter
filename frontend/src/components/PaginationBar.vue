<script setup>
import { computed } from 'vue'

const props = defineProps({
  page: { type: Number, required: true },
  pageCount: { type: Number, required: true },
  total: { type: Number, default: 0 },
})

const emit = defineEmits(['update:page'])

const canPrev = computed(() => props.page > 1)
const canNext = computed(() => props.page < props.pageCount)
</script>

<template>
  <nav class="pager" aria-label="分页">
    <p class="pager__total">
      共 <strong>{{ total }}</strong> 场
      <span class="pager__sep" aria-hidden="true">·</span>
      第 {{ page }} / {{ pageCount }} 页
    </p>

    <div class="pager__controls">
      <button
        class="btn btn--ghost"
        type="button"
        :disabled="!canPrev"
        @click="emit('update:page', page - 1)"
      >
        上一页
      </button>
      <button
        class="btn btn--ghost"
        type="button"
        :disabled="!canNext"
        @click="emit('update:page', page + 1)"
      >
        下一页
      </button>
    </div>
  </nav>
</template>

<style scoped>
.pager {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-top: 26px;
  padding-top: 20px;
  border-top: 1px solid var(--border);
}

.pager__total {
  font-size: 13.5px;
  color: var(--text-soft);
  font-variant-numeric: tabular-nums;
}

.pager__total strong {
  color: var(--text);
}

.pager__sep {
  margin: 0 4px;
  color: var(--text-faint);
}

.pager__controls {
  display: flex;
  gap: 8px;
}
</style>
