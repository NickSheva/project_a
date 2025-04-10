import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urljoin
import time
from prettytable import PrettyTable


BASE_URL = "https://lombard-perspectiva.ru"

async def get_product_links(page):
    """Получает все ссылки на товары со страницы"""
    await page.wait_for_selector('a.product-list-item', state="attached")
    product_links = await page.locator('a.product-list-item').evaluate_all(
        "elements => elements.map(el => el.getAttribute('href'))"
    )
    return [urljoin(BASE_URL, link) for link in product_links]

async def main():
    """Основная асинхронная функция"""
    full_links = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # headless=False для отладки
        page = await browser.new_page()
        
        url = f"{BASE_URL}/clocks_today/?page=1"
        
        start_time = time.time()
        
        await page.goto(url, wait_until="domcontentloaded")
        full_links = await get_product_links(page)
        table = PrettyTable()
        table.field_names = (["#", "LINKS"])
        table.align["LINKS"] = "l"
        for i, link in enumerate(full_links, 1):
            table.add_row([i, link])
        
        print(f"--- {time.time() - start_time:.2f} seconds ---")
        
        await browser.close()
    
    return table

if __name__ == "__main__":
    print(asyncio.run(main()))