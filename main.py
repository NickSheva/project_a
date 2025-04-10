import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urljoin
import time
from prettytable import PrettyTable


import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urljoin
import time

BASE_URL = "https://lombard-perspectiva.ru"

async def get_product_links(page):
    """Получает все ссылки на товары со страницы"""
    await page.wait_for_selector('a.product-list-item', state="attached")
    product_links = await page.locator('a.product-list-item').evaluate_all(
        "elements => elements.map(el => el.getAttribute('href'))"
    )
    return [urljoin(BASE_URL, link) for link in product_links]

async def main(page_number=1):
    """Основная асинхронная функция"""
    full_links = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # headless=False для отладки
        page = await browser.new_page()
        
        url = f"{BASE_URL}/clocks_today/?page={page_number}"
        
        start_time = time.time()
        
        try:
            await page.goto(url, wait_until="domcontentloaded")
            full_links = await get_product_links(page)
            print(f"Успешно спарсено {len(full_links)} товаров со страницы {page_number}")
        except Exception as e:
            print(f"Ошибка при парсинге страницы {page_number}: {e}")
        finally:
            table = PrettyTable()
            table.field_names = (["№", "LINKS"])
            table.align["LINKS"] = "c"
            for i, link in enumerate(full_links, 1):
                table.add_row([i, link])
            
            print(f"--- {time.time() - start_time:.2f} seconds ---")
            await browser.close()
    
    return table

if __name__ == "__main__":
    # Запрос номера страницы у пользователя
    page_number = input("Введите номер страницы для парсинга (по умолчанию 1): ") or 1
    try:
        page_number = int(page_number)
    except ValueError:
        print("Некорректный номер страницы. Будет использована страница 1")
        page_number = 1
    
    # Запуск парсинга
    result = asyncio.run(main(page_number))
    print(f"Результат парсинга (первые 5 ссылок): {result[:5]}")
