<script setup>
import AppHeader from './components/AppHeader.vue'
import ExhibitionGrid from './components/ExhibitionGrid.vue'
import HeroPanel from './components/HeroPanel.vue'
import PaginationBar from './components/PaginationBar.vue'
import { useExhibitionList } from './composables/useExhibitionList'
import { t } from './i18n'

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
        <p>{{ t('footer.source') }}</p>
        <p>{{ t('footer.api', { path: '/api/exhibitions' }) }}</p>
      </div>
    </footer>
  </div>
</template>
