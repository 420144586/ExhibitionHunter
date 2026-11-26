<script setup>
import AppHeader from './components/AppHeader.vue'
import ExhibitionGrid from './components/ExhibitionGrid.vue'
import HeroPanel from './components/HeroPanel.vue'
import PaginationBar from './components/PaginationBar.vue'
import { useExhibitionList } from './composables/useExhibitionList'

const {
  query,
  items,
  total,
  loading,
  error,
  pageCount,
  hasFilters,
  setStatus,
  setKeyword,
  setPage,
  retry,
  clearFilters,
} = useExhibitionList()
</script>

<template>
  <div class="page">
    <AppHeader :total="total" :loading="loading" />

    <main class="page__main">
      <HeroPanel
        :status="query.status"
        :keyword="query.keyword"
        @update:status="setStatus"
        @update:keyword="setKeyword"
      />

      <ExhibitionGrid
        :items="items"
        :loading="loading"
        :error="error"
        :has-filters="hasFilters"
        :page-size="query.page_size"
        @retry="retry"
        @clear="clearFilters"
      />

      <PaginationBar
        v-if="!loading && !error && total > 0"
        :page="query.page"
        :page-count="pageCount"
        :total="total"
        @update:page="setPage"
      />
    </main>

    <footer class="site-footer">
      <div class="container site-footer__inner">
        <p>数据来源：淘展云 · 每日 03:00 自动抓取</p>
        <p>接口 <code>/api/exhibitions</code> · 只列出尚未结束的展会</p>
      </div>
    </footer>
  </div>
</template>
