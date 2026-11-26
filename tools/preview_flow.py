"""开发期交互自检：验证首页的四种关键状态。

用法（在仓库根目录执行）：
    backend\\.venv\\Scripts\\python.exe tools\\preview_flow.py http://127.0.0.1:5174 .tmp-dev

覆盖：切换到「即将开始」、搜索无结果、后端口不可达时的错误态、移动端布局。
"""
import asyncio
import glob
import os
import re
import sys

from playwright.async_api import async_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5174"
OUT_DIR = sys.argv[2] if len(sys.argv) > 2 else ".tmp-dev"


def find_executable() -> str | None:
    base = os.path.join(os.environ.get("LOCALAPPDATA", ""), "ms-playwright")
    patterns = [
        "chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe",
        "chromium_headless_shell-*/chrome-win/headless_shell.exe",
        "chromium-*/chrome-win64/chrome.exe",
        "chromium-*/chrome-win/headless.exe",
    ]
    for pattern in patterns:
        hits = glob.glob(os.path.join(base, pattern))
        if hits:
            return sorted(hits)[-1]
    return None


async def launch(p):
    try:
        return await p.chromium.launch(headless=True)
    except Exception:  # noqa: BLE001
        executable = find_executable()
        if not executable:
            raise
        return await p.chromium.launch(headless=True, executable_path=executable)


async def collect(page):
    return {
        "cards": await page.locator(".card").count(),
        "pills": await page.locator(".card .pill").all_inner_texts(),
        "pager": (await page.locator(".pager__total").inner_text()).strip()
        if await page.locator(".pager__total").count()
        else "",
        "state_title": (await page.locator(".state__title").inner_text()).strip()
        if await page.locator(".state__title").count()
        else "",
    }


async def main() -> int:
    async with async_playwright() as p:
        browser = await launch(p)
        page = await browser.new_page(viewport={"width": 1440, "height": 1100})

        await page.goto(URL, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(1200)

        # 1) 切换到「即将开始」
        await page.get_by_role("tab", name="即将开始").click()
        await page.wait_for_timeout(1500)
        info = await collect(page)
        print("TAB_UPCOMING cards=", info["cards"], "pills=", set(info["pills"]), "pager=", info["pager"])
        await page.screenshot(path=os.path.join(OUT_DIR, "state-upcoming.png"), full_page=True)

        # 2) 搜索一个必然无结果的关键词
        await page.fill(".search__input", "不存在的展会zzz")
        await page.press(".search__input", "Enter")
        await page.wait_for_timeout(1500)
        info = await collect(page)
        print("EMPTY cards=", info["cards"], "state=", info["state_title"])
        await page.screenshot(path=os.path.join(OUT_DIR, "state-empty.png"), full_page=True)

        # 3) 模拟后端不可达：只拦真实接口路径，别把 /src/api/*.js 模块也拦掉
        await page.route(re.compile(r"^https?://[^/]+/api/"), lambda route: route.abort())
        await page.reload(wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        info = await collect(page)
        print("ERROR cards=", info["cards"], "state=", info["state_title"])
        await page.screenshot(path=os.path.join(OUT_DIR, "state-error.png"), full_page=True)

        # 4) 移动端首屏
        mobile = await browser.new_page(viewport={"width": 390, "height": 844})
        await mobile.goto(URL, wait_until="networkidle", timeout=30000)
        await mobile.wait_for_timeout(1500)
        mobile_info = await collect(mobile)
        overflow = await mobile.evaluate(
            "() => document.documentElement.scrollWidth > window.innerWidth"
        )
        print("MOBILE cards=", mobile_info["cards"], "horizontal_overflow=", overflow)
        await mobile.screenshot(path=os.path.join(OUT_DIR, "state-mobile.png"), full_page=True)

        await browser.close()
        return 0


sys.exit(asyncio.run(main()))
