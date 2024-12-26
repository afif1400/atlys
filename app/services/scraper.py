from typing import Optional
import requests
from bs4 import BeautifulSoup
import os
from time import sleep
from app.services.cache import CacheService

class Scraper:
    def __init__(self, base_url: str, max_pages: Optional[int] = None, proxy: Optional[str] = None):
        self.base_url = base_url
        self.max_pages = max_pages
        self.proxy = proxy
        self.session = requests.Session()
        self.cache = CacheService()
        if proxy:
            self.session.proxies = {"https": proxy, "http": proxy}

    async def scrape(self):
        scraped_data = []
        page = 1

        while True:
            if self.max_pages and page > self.max_pages:
                break

            url = f"{self.base_url}/page/{page}/"
            try:
                print(f"Scraping: {url}")
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching {url}: {e}")
                sleep(5) # wait 5 seconds before retrying
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.select("li[class*='product']")

            if not products:
                print("No more products found.")
                break

            for product in products:
                name_element = product.select_one(".mf-product-details .mf-product-content h2")
                if not name_element:
                    print("Could not find product name")
                    continue
                price_element = product.select_one(".mf-product-details .mf-product-price-box .price")
                image_element = product.select_one(".mf-product-thumbnail a img")

                price_value = 0.0
                if price_element:
                    actual_price = price_element.select_one("ins .woocommerce-Price-amount bdi")
                    if actual_price:
                        price_text = actual_price.text.strip()
                        price_value = float(price_text.replace('₹', '').replace(',', '').strip())
                    else:
                        regular_price = price_element.select_one(".woocommerce-Price-amount bdi")
                        if regular_price:
                            price_text = regular_price.text.strip()
                            price_value = float(price_text.replace('₹', '').replace(',', '').strip())
                        else:
                            price_value = 0.0
                name = name_element.text.strip()
                cached = self.cache.get(name)
                if cached:
                    print(f"Product {name} already scraped. Skipping.")
                    continue
                image_path = self.download_image(image_element, name)

                scraped_data.append({
                    "product_title": name,
                    "product_price": price_value,
                    "path_to_image": image_path
                })
                self.cache.set(name, image_path)

            page += 1

        return scraped_data

    def download_image(self, img_element, product_name: str) -> str:
        image_url = self.get_image_url(img_element)
        if not image_url:
            print(f"Could not find image URL for {product_name}")
            return ""

        image_filename = f"{product_name.replace(' ', '_').replace('/', '_')}.jpg"
        image_path = os.path.join("images", image_filename)
        os.makedirs("images", exist_ok=True)

        try:
            response = self.session.get(image_url, stream=True, timeout=10)
            response.raise_for_status()
            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return image_path
        except requests.exceptions.RequestException as e:
            print(f"Failed to download image {image_url}: {e}")
            return ""

    def get_image_url(self, img_element):
        """Extract the actual image URL from lazy-loaded image element"""
        image_url = img_element.get('data-lazy-src')

        if not image_url:
            srcset = img_element.get('data-lazy-srcset')
            if srcset:
                image_url = srcset.split(',')[0].split()[0]

        if not image_url:
            image_url = img_element.get('src')

        return image_url
