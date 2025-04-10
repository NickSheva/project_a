from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
import time

BASE_URL = "https://lombard-perspectiva.ru"

def main():
    """Парсинг ссылок на карточки товара с первой страницы каталога с использованием Playwright"""
    full_links = []
    
    with sync_playwright() as p:
        # Запускаем браузер (можно использовать 'chromium', 'firefox' или 'webkit')
        browser = p.chromium.launch(headless=True)  # headless=False для визуального отображения
        page = browser.new_page()
        
        url = f"{BASE_URL}/clocks_today/?page=1"
        
        start_time = time.time()
        
        # Переходим на страницу
        page.goto(url, wait_until="domcontentloaded")
        
        # Ждем загрузки элементов (опционально)
        page.wait_for_selector('a.product-list-item', state="attached")
        
        # Получаем все ссылки на товары
        product_links = page.locator('a.product-list-item').evaluate_all(
            "elements => elements.map(el => el.getAttribute('href'))"
        )
        
        full_links = [urljoin(BASE_URL, link) for link in product_links]
        
        print("--- %s seconds ---" % (time.time() - start_time))
        
        browser.close()
    
    return full_links

if __name__ == "__main__":
    print(main())