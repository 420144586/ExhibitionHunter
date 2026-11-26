"""开发期自检脚本：用 Playwright 打开本地页面，抓取渲染结果并截图。

用法（在仓库根目录执行）：
    backend\\.venv\\Scripts\\python.exe tools\\preview_check.py http://127.0.0.1:5173 preview.png

它验证的是「页面真的渲染出了卡片」这件事，而不是只看构建是否通过。
本机 playwright 版本与已下载的浏览器版本可能不一致，因此启动失败时
会自动回退到 ms-playwright 目录里已存在的 chromium 可执行文件。
"""
import asyncio
import glob
import os
import sys

from playwright.async_api import async_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5173"
OUT = sys.argv[2] if len(sys.argv) > 2 else "preview.png"


def find_executable() -> str | None:
    """在 ms-playwright 目录里找一个可用的 chromium 可执行文件（取版本号最大的）。"""
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
    except Exception as default_error:  # noqa: BLE001
        executable = find_executable()
        if not executable:
            raise
        print("FALLBACK_EXECUTABLE:", executable)
        try:
            return await p.chromium.launch(headless=True, executable_path=executable)
        except Exception as fallback_error:  # noqa: BLE001
            print("DEFAULT_LAUNCH_ERROR:", str(default_error).splitlines()[0])
            raise fallback_error


async def main() -> int:
    async with async_playwright() as p:
        try:
            browser = await launch(p)
        except Exception as exc:  # noqa: BLE001
            print("CHROMIUM_MISSING:", str(exc).splitlines()[0])
            return 2

        page = await browser.new_page(viewport={"width": 1440, "height": 1100})
        issues: list[str] = []
        page.on(
            "console",
            lambda msg: issues.append(f"{msg.type}: {msg.text}")
            if msg.type in ("error", "warning")
            else None,
        )
        page.on("pageerror", lambda exc: issues.append(f"pageerror: {exc}"))

        await page.goto(URL, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(1500)

        async def text_of(selector: str) -> str:
            locator = page.locator(selector)
            if await locator.count() == 0:
                return ""
            return (await locator.first.inner_text()).strip()

        print("TITLE:", await page.title())
        print("CARDS:", await page.locator(".card").count())
        print("SKELETONS:", await page.locator(".skeleton").count())
        print("STATE_PANELS:", await page.locator(".state").count())
        print("FIRST_TITLE:", await text_of(".card__title"))
        print("FIRST_RANGE:", await text_of(".card__range"))
        print("FIRST_PILL:", await text_of(".card .pill"))
        print("HEADER_STAT:", await text_of(".site-header__stat"))
        print("PAGER:", await text_of(".pager__total"))
        if issues:
            print("CONSOLE_ISSUES:", issues[:6])

        await page.screenshot(path=OUT, full_page=True)
        print("SHOT:", OUT)
        await browser.close()
        return 0


sys.exit(asyncio.run(main()))
