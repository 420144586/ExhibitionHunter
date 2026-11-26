"""语言切换自检：中文默认、切英文、刷新后保持、移动端英文布局。

用法（仓库根目录）：
    backend\\.venv\\Scripts\\python.exe tools\\preview_i18n.py http://127.0.0.1:5174 .tmp-dev
"""
import asyncio
import glob
import os
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
        "chromium-*/chrome-win/chrome.exe",
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


async def snapshot(page):
    async def text_of(selector: str) -> str:
        locator = page.locator(selector)
        if await locator.count() == 0:
            return ""
        return (await locator.first.inner_text()).strip().replace("\n", " ")

    return {
        "html_lang": await page.evaluate("document.documentElement.lang"),
        "title": await page.title(),
        "hero": await text_of(".hero__title"),
        "tabs": (await page.locator(".tabs__tab").all_inner_texts()),
        "list": await text_of(".list__title"),
        "first_pill": await text_of(".card .pill"),
        "first_range": await text_of(".card__range"),
        "pager": await text_of(".pager__total"),
        "footer": await text_of(".site-footer p"),
        "cards": await page.locator(".card").count(),
    }


async def main() -> int:
    async with async_playwright() as p:
        browser = await launch(p)
        page = await browser.new_page(viewport={"width": 1440, "height": 1100})

        await page.goto(URL, wait_until="domcontentloaded", timeout=30000)
        # 固定初始语言为中文，避免受机器语言影响
        await page.evaluate("localStorage.setItem('eh.locale', 'zh')")
        await page.reload(wait_until="networkidle")
        await page.wait_for_timeout(1200)

        print("ZH:", await snapshot(page))
        await page.screenshot(path=os.path.join(OUT_DIR, "i18n-zh.png"), full_page=True)

        await page.get_by_role("button", name="EN", exact=True).click()
        await page.wait_for_timeout(900)
        print("EN:", await snapshot(page))
        await page.screenshot(path=os.path.join(OUT_DIR, "i18n-en.png"), full_page=True)

        # 刷新后应保持英文
        await page.reload(wait_until="networkidle")
        await page.wait_for_timeout(1200)
        after = await snapshot(page)
        print("EN_AFTER_RELOAD:", after["html_lang"], "/", after["hero"])

        # 移动端英文
        mobile = await browser.new_page(viewport={"width": 390, "height": 844})
        await mobile.goto(URL, wait_until="domcontentloaded")
        await mobile.evaluate("localStorage.setItem('eh.locale', 'en')")
        await mobile.reload(wait_until="networkidle")
        await mobile.wait_for_timeout(1200)
        overflow = await mobile.evaluate(
            "() => document.documentElement.scrollWidth > window.innerWidth"
        )
        print("MOBILE_EN: cards=", await mobile.locator(".card").count(), " overflow=", overflow)
        await mobile.screenshot(path=os.path.join(OUT_DIR, "i18n-en-mobile.png"), full_page=True)

        await browser.close()
        return 0


sys.exit(asyncio.run(main()))
