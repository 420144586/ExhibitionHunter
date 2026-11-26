<script setup>
defineProps({
  kind: { type: String, default: 'empty' },
  title: { type: String, default: '' },
  message: { type: String, default: '' },
  actionLabel: { type: String, default: '' },
  secondaryLabel: { type: String, default: '' },
})

defineEmits(['action', 'secondary'])
</script>

<template>
  <div class="state" :class="`state--${kind}`" role="status">
    <span class="state__icon" aria-hidden="true">
      <svg v-if="kind === 'error'" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.7" />
        <path d="M12 7.6v5.2" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" />
        <circle cx="12" cy="16.3" r="1.05" fill="currentColor" />
      </svg>
      <svg v-else viewBox="0 0 24 24">
        <circle cx="11" cy="11" r="6.6" fill="none" stroke="currentColor" stroke-width="1.7" />
        <path d="M16.2 16.2 20.4 20.4" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" />
      </svg>
    </span>

    <h3 class="state__title">{{ title }}</h3>
    <p v-if="message" class="state__message">{{ message }}</p>

    <div v-if="actionLabel || secondaryLabel" class="state__actions">
      <button v-if="actionLabel" class="btn btn--primary" type="button" @click="$emit('action')">
        {{ actionLabel }}
      </button>
      <button
        v-if="secondaryLabel"
        class="btn btn--ghost"
        type="button"
        @click="$emit('secondary')"
      >
        {{ secondaryLabel }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 64px 24px;
  border: 1px dashed var(--border-strong);
  border-radius: var(--radius-lg);
  background: var(--surface);
}

.state__icon {
  display: grid;
  place-items: center;
  width: 46px;
  height: 46px;
  margin-bottom: 14px;
  border-radius: 999px;
  background: var(--surface-2);
  color: var(--text-faint);
}

.state--error .state__icon {
  background: var(--danger-soft);
  color: var(--danger);
}

.state__icon svg {
  width: 24px;
  height: 24px;
}

.state__title {
  font-size: 17px;
  font-weight: 620;
  color: var(--text);
}

.state__message {
  margin-top: 8px;
  max-width: 46ch;
  font-size: 14px;
  color: var(--text-soft);
  line-height: 1.65;
}

.state__actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
}
</style>
