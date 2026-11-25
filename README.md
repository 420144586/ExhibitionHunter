# ExhibitionHunter

展会信息聚合与检索系统：爬取全国正在展出 / 即将展出的展会数据，前端展示 + 后端爬虫 + REST API。

## 目录结构

```
ExhibitionHunter/
├─ frontend/   # Vite + Vue 3 前端
└─ backend/    # FastAPI + 爬虫后端
```

## 快速开始

### 后端

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
# http://localhost:8000/docs
```

数据源：淘展云 (taozhanyun.com)，每日 03:00 自动爬取正在展出 + 未来 3 个月展会。

主要接口：
- `GET /api/exhibitions?status=ongoing|upcoming|all&page=&page_size=&city=&industry=&keyword=`
- `POST /api/exhibitions/crawl` 手动触发爬取
- `GET /health` 健康检查

### 前端

```powershell
cd frontend
npm install
npm run dev
# http://localhost:5173
```

## 技术栈

- 后端：FastAPI / httpx + selectolax / SQLAlchemy 2.0 (async) + SQLite / APScheduler / Pydantic v2 / loguru
- 前端：Vite + Vue 3
