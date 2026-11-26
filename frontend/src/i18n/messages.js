/**
 * 界面文案。key 用扁平点号命名，{name} 为插值占位符。
 * 新增文案时中英两套都要加，缺 key 时 t() 会回退到中文再回退到 key 本身。
 */
export const SUPPORTED_LOCALES = ['zh', 'en']

export const messages = {
  zh: {
    'meta.title': '展会猎人 · 正在展出与即将开始的展会',

    'header.brandSub': 'EXHIBITIONHUNTER',
    'header.syncing': '正在同步',
    'header.count': '当前 {n} 场在展或即将开始',
    'header.hint': '数据每日 03:00 自动更新',
    'header.langLabel': '切换语言',

    'hero.eyebrow': '全国展会 · 每日聚合',
    'hero.title': '找到下一场值得去的展会',
    'hero.lede':
      '只收录正在展出与即将开始的展会，按开幕时间排序。数据来自公开展会信息站，每天凌晨自动更新。',
    'hero.searchPlaceholder': '搜索展会名称，例如：食品、机床、家居',
    'hero.searchLabel': '搜索展会名称',
    'hero.search': '搜索',
    'hero.clearSearch': '清空搜索',
    'hero.statusLabel': '按展出状态筛选',

    'tabs.all': '全部在展',
    'tabs.ongoing': '正在展出',
    'tabs.upcoming': '即将开始',

    'list.title': '近期展会',
    'list.hint': '按开幕时间由近到远',

    'status.ongoing': '展出中',
    'status.upcoming': '即将开始',
    'status.ended': '已结束',

    'card.placeTbd': '地点待定',
    'card.rangeTbd': '展期待定',
    'card.days': '{n} 天',

    'countdown.opensToday': '今天开幕',
    'countdown.opensTomorrow': '明天开幕',
    'countdown.opensInDays': '{n} 天后开幕',
    'countdown.closesToday': '今天闭幕',
    'countdown.closesTomorrow': '明天闭幕',
    'countdown.daysLeft': '还有 {n} 天',

    'error.network.title': '连不上后端服务',
    'error.network.message':
      '请确认 API 已启动：在 backend 目录执行 uvicorn app.main:app --port 8000，然后重试。',
    'error.timeout.title': '请求超时',
    'error.timeout.message': '后端响应过慢，请稍后重试。',
    'error.invalid.title': '筛选条件不合法',
    'error.invalid.message': '请调整条件后重试。',
    'error.parse.title': '返回数据无法解析',
    'error.parse.message': '请检查后端接口输出。',
    'error.http.title': '服务返回错误',
    'error.http.message': '请稍后重试。',

    'empty.filtered.title': '没有符合条件的展会',
    'empty.filtered.message': '换个关键词，或切回「全部在展」看看。',
    'empty.nodata.title': '还没有采集到展会',
    'empty.nodata.message':
      '数据库里暂时没有未结束的展会。可以手动触发一次抓取：POST /api/exhibitions/crawl，完成后刷新本页。',

    'action.retry': '重试',
    'action.reload': '重新加载',
    'action.clearFilters': '清除筛选',

    'pager.summary': '共 {total} 场 · 第 {page} / {pages} 页',
    'pager.prev': '上一页',
    'pager.next': '下一页',

    'footer.source': '数据来源：淘展云 · 每日 03:00 自动抓取',
    'footer.api': '接口 {path} · 只列出尚未结束的展会',
  },

  en: {
    'meta.title': 'ExhibitionHunter · Shows on now and coming up',

    'header.brandSub': 'EXHIBITIONHUNTER',
    'header.syncing': 'Syncing',
    'header.count': '{n} shows on now or upcoming',
    'header.hint': 'Updated daily at 03:00',
    'header.langLabel': 'Switch language',

    'hero.eyebrow': 'Trade shows · aggregated daily',
    'hero.title': 'Find the next show worth your time',
    'hero.lede':
      'Only shows that are running now or about to open, sorted by opening date. Sourced from public exhibition listings and refreshed every night.',
    'hero.searchPlaceholder': 'Search by show name, e.g. food, machine tools, furniture',
    'hero.searchLabel': 'Search by show name',
    'hero.search': 'Search',
    'hero.clearSearch': 'Clear search',
    'hero.statusLabel': 'Filter by show status',

    'tabs.all': 'All active',
    'tabs.ongoing': 'On now',
    'tabs.upcoming': 'Opening soon',

    'list.title': 'Shows',
    'list.hint': 'Sorted by opening date',

    'status.ongoing': 'On now',
    'status.upcoming': 'Opening soon',
    'status.ended': 'Ended',

    'card.placeTbd': 'Venue to be confirmed',
    'card.rangeTbd': 'Dates to be confirmed',
    'card.days': '{n} days',

    'countdown.opensToday': 'Opens today',
    'countdown.opensTomorrow': 'Opens tomorrow',
    'countdown.opensInDays': 'Opens in {n} days',
    'countdown.closesToday': 'Closes today',
    'countdown.closesTomorrow': 'Closes tomorrow',
    'countdown.daysLeft': '{n} days left',

    'error.network.title': "Can't reach the API",
    'error.network.message':
      'Start the backend first: run uvicorn app.main:app --port 8000 inside the backend directory, then retry.',
    'error.timeout.title': 'Request timed out',
    'error.timeout.message': 'The backend took too long to respond. Please retry.',
    'error.invalid.title': 'Invalid filter',
    'error.invalid.message': 'Adjust the filters and try again.',
    'error.parse.title': 'Unreadable response',
    'error.parse.message': 'Check what the backend returned.',
    'error.http.title': 'The service returned an error',
    'error.http.message': 'Please retry in a moment.',

    'empty.filtered.title': 'No shows match these filters',
    'empty.filtered.message': 'Try another keyword, or switch back to “All active”.',
    'empty.nodata.title': 'Nothing collected yet',
    'empty.nodata.message':
      'There are no active shows in the database. Trigger a crawl with POST /api/exhibitions/crawl, then reload this page.',

    'action.retry': 'Retry',
    'action.reload': 'Reload',
    'action.clearFilters': 'Clear filters',

    'pager.summary': '{total} shows · page {page} of {pages}',
    'pager.prev': 'Previous',
    'pager.next': 'Next',

    'footer.source': 'Source: taozhanyun.com · crawled daily at 03:00',
    'footer.api': 'Endpoint {path} · only shows that have not ended',
  },
}
