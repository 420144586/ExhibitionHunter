# ExhibitionHunter Backend

展会数据爬虫 + REST API 服务。

## 技术栈

- **FastAPI** — 异步 API 框架，自带 OpenAPI 文档 (`/docs`)
- **httpx + selectolax** — 静态页面抓取与解析
- **Playwright** — 动态 JS 渲染页面抓取（按需启用）
- **SQLAlchemy 2.0 (async) + SQLite** — 数据存储
- **APScheduler** — 定时爬取任务
- **Pydantic v2 / loguru** — 数据校验与日志

## 目录结构

```
backend/
├─ app/
│  ├─ main.py              # FastAPI 入口
│  ├─ api/                 # 路由
│  ├─ core/                # 配置 / 数据库 / 日志
│  ├─ models/              # SQLAlchemy 模型
│  ├─ schemas/             # Pydantic 模型
│  ├─ services/            # 业务逻辑
│  └─ crawler/             # 爬虫
│     ├─ base.py           # BaseSpider 抽象
│     ├─ pipelines.py      # 清洗 / 去重 / 入库
│     ├─ scheduler.py      # 定时任务
│     └─ sites/            # 每个站点一个 spider
├─ data/                   # SQLite & 日志（运行时生成）
├─ .env.example
└─ requirements.txt
```

## 快速开始

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# 可选：安装 Playwright 浏览器（仅动态渲染需要）
playwright install chromium

copy .env.example .env       # Windows
# cp .env.example .env       # Linux/Mac

uvicorn app.main:app --reload --port 8000
```

打开 http://localhost:8000/docs 查看交互式 API 文档。

## 使用

- `GET /api/exhibitions` — 分页查询展会列表
  - 参数：`page`, `page_size`, `city`, `industry`, `keyword`
- `POST /api/exhibitions/crawl` — 手动触发全站爬取
- `GET /health` — 健康检查

## 添加新爬虫

1. 在 `app/crawler/sites/` 下新建文件，继承 `BaseSpider`
2. 实现 `parse()` 方法，使用 `selectolax` 解析 HTML 并 `yield ExhibitionCreate`
3. 在 `app/crawler/sites/__init__.py` 的 `ALL_SPIDERS` 列表注册

```python
from app.crawler.base import BaseSpider
from app.schemas.exhibition import ExhibitionCreate

class MySiteSpider(BaseSpider):
    name = "mysite"
    start_urls = ["https://mysite.com/exhibitions"]
    engine = "auto"  # 或 "playwright" 强制动态渲染

    async def parse(self, html, url):
        # ...
        yield ExhibitionCreate(source_site=self.name, source_id=..., ...)
```

## 配置项

见 `.env.example`：

| 变量 | 说明 |
|---|---|
| `DATABASE_URL` | SQLite 路径 |
| `CRAWLER_DEFAULT_ENGINE` | `auto` / `httpx` / `playwright` |
| `CRAWLER_MAX_CONCURRENCY` | 单次爬取并发上限 |
| `SCHEDULER_ENABLED` | 启动时是否开启定时任务 |
| `SCHEDULER_CRAWL_CRON` | cron 表达式，如 `0 3 * * *`（每日 3 点） |
| `LOG_LEVEL` / `LOG_DIR` | 日志级别与目录 |
