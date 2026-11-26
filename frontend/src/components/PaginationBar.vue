<script setup>
import { computed } from 'vue'
import { t } from '../i18n'

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
  <nav class="pager" aria-label="pagination">
    <p class="pager__total">
      {{ t('pager.summary', { total, page, pages: pageCount }) }}
    </p>

    <div class="pager__controls">
      <button
        class="btn btn--ghost"
        type="button"
        :disabled="!canPrev"
        @click="emit('update:page', page - 1)"
      >
        {{ t('pager.prev') }}
      </button>
      <button
        class="btn btn--ghost"
        type="button"
        :disabled="!canNext"
        @click="emit('update:page', page + 1)"
      >
        {{ t('pager.next') }}
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

.pager__controls {
  display: flex;
  gap: 8px;
}
</style>
