<script setup>
defineProps({
  count: { type: Number, default: 6 },
})
</script>

<template>
  <div class="skeletons" aria-hidden="true">
    <div v-for="index in count" :key="index" class="skeleton">
      <div class="skeleton__aside">
        <span class="skeleton__block skeleton__block--badge"></span>
        <span class="skeleton__block skeleton__block--pill"></span>
      </div>
      <div class="skeleton__body">
        <span class="skeleton__block skeleton__block--title"></span>
        <span class="skeleton__block skeleton__block--line"></span>
        <span class="skeleton__block skeleton__block--line skeleton__block--short"></span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.skeletons {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(430px, 1fr));
  gap: 14px;
}

.skeleton {
  display: flex;
  gap: 16px;
  padding: 16px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
}

.skeleton__aside {
  flex: 0 0 78px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.skeleton__body {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  gap: 9px;
  padding-top: 4px;
}

.skeleton__block {
  display: block;
  border-radius: 6px;
  background: linear-gradient(90deg, var(--surface-2) 25%, var(--bg-soft) 50%, var(--surface-2) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
}

.skeleton__block--badge {
  width: 100%;
  height: 70px;
  border-radius: var(--radius-sm);
}

.skeleton__block--pill {
  width: 56px;
  height: 20px;
  border-radius: 999px;
}

.skeleton__block--title {
  width: 82%;
  height: 20px;
}

.skeleton__block--line {
  width: 60%;
  height: 14px;
}

.skeleton__block--short {
  width: 38%;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

@media (max-width: 640px) {
  .skeletons {
    grid-template-columns: 1fr;
  }
}
</style>
