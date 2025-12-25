"""
Arkham Horror LCG Game Store Scraper

This module provides functionality to search for game stores in a specified area
and check their inventory for Arkham Horror LCG products.
"""

import time
import re
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class ArkhamHorrorStoreScanner:
    """Scanner for finding Arkham Horror LCG products in game stores."""
    
    def __init__(self, headless: bool = True):
        """
        Initialize the store scanner.
        
        Args:
            headless: Whether to run browser in headless mode
        """
        self.headless = headless
        self.driver = None
        self.arkham_keywords = [
            "arkham horror",
            "arkham horror lcg",
            "arkham horror: the card game",
            "arkham horror card game",
            "fantasy flight arkham"
        ]
    
    def setup_driver(self):
        """Set up the Selenium WebDriver."""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)
    
    def close_driver(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def search_game_stores(self, location: str) -> List[Dict[str, str]]:
        """
        Search for game stores in the specified location using Google Maps.
        
        Args:
            location: The location to search (e.g., "Seattle, WA" or "90210")
        
        Returns:
            List of dictionaries containing store information
        """
        stores = []
        
        try:
            # Search on Google Maps for game stores
            search_query = f"board game stores near {location}"
            google_search_url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
            
            self.driver.get(google_search_url)
            time.sleep(3)  # Wait for results to load
            
            # Try to find store listings
            # Google Maps structure can vary, so we'll try multiple selectors
            try:
                # Wait for results to appear
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='feed']"))
                )
                time.sleep(2)
                
                # Get store elements
                store_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")
                
                # Limit to first 10 stores to avoid excessive scraping
                for store_elem in store_elements[:10]:
                    try:
                        store_info = self._extract_store_info_from_maps(store_elem)
                        if store_info:
                            stores.append(store_info)
                    except Exception as e:
                        print(f"Error extracting store info: {e}")
                        continue
                        
            except TimeoutException:
                print(f"Timeout waiting for search results for location: {location}")
        
        except Exception as e:
            print(f"Error searching for stores: {e}")
        
        return stores
    
    def _extract_store_info_from_maps(self, element) -> Optional[Dict[str, str]]:
        """
        Extract store information from a Google Maps element.
        
        Args:
            element: Selenium WebElement containing store data
        
        Returns:
            Dictionary with store information or None
        """
        store_info = {
            'name': '',
            'address': '',
            'phone': '',
            'website': '',
            'maps_url': ''
        }
        
        try:
            # Try to extract store name
            try:
                name_elem = element.find_element(By.CSS_SELECTOR, "div.fontHeadlineSmall")
                store_info['name'] = name_elem.text
            except NoSuchElementException:
                pass
            
            # Click on the store to get more details
            try:
                element.click()
                time.sleep(2)
                
                # Extract phone number
                try:
                    phone_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-item-id^='phone']")
                    phone_text = phone_button.get_attribute("data-item-id")
                    if phone_text:
                        # Extract phone from data attribute
                        phone_match = re.search(r'phone:tel:(.+)', phone_text)
                        if phone_match:
                            store_info['phone'] = phone_match.group(1)
                except NoSuchElementException:
                    pass
                
                # Extract website
                try:
                    website_button = self.driver.find_element(By.CSS_SELECTOR, "a[data-item-id='authority']")
                    store_info['website'] = website_button.get_attribute("href")
                except NoSuchElementException:
                    pass
                
                # Extract address
                try:
                    address_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-item-id='address']")
                    store_info['address'] = address_button.get_attribute("aria-label")
                except NoSuchElementException:
                    pass
                
                # Get the current URL as maps URL
                store_info['maps_url'] = self.driver.current_url
                
            except Exception as e:
                print(f"Error clicking element or extracting details: {e}")
        
        except Exception as e:
            print(f"Error in _extract_store_info_from_maps: {e}")
        
        return store_info if store_info['name'] else None
    
    def check_store_inventory(self, store_info: Dict[str, str]) -> Dict[str, any]:
        """
        Check if a store has Arkham Horror LCG products.
        
        Args:
            store_info: Dictionary containing store information
        
        Returns:
            Dictionary with store info and product availability
        """
        result = {
            'store_name': store_info.get('name', 'Unknown'),
            'website': store_info.get('website', 'N/A'),
            'phone': store_info.get('phone', 'N/A'),
            'address': store_info.get('address', 'N/A'),
            'maps_url': store_info.get('maps_url', 'N/A'),
            'has_arkham_products': False,
            'products_found': [],
            'search_attempted': False
        }
        
        website = store_info.get('website', '')
        
        # Skip if no website
        if not website or website == 'N/A':
            return result
        
        try:
            result['search_attempted'] = True
            self.driver.get(website)
            time.sleep(2)
            
            # Get page source and search for Arkham Horror keywords
            page_source = self.driver.page_source.lower()
            
            # Check for Arkham Horror mentions
            for keyword in self.arkham_keywords:
                if keyword.lower() in page_source:
                    result['has_arkham_products'] = True
                    break
            
            # Try to find search functionality and search for Arkham Horror
            if self._try_site_search(website):
                # If we successfully searched, check results
                time.sleep(2)
                page_source = self.driver.page_source.lower()
                
                if "arkham horror" in page_source:
                    result['has_arkham_products'] = True
                    
                    # Try to extract product information
                    products = self._extract_products()
                    if products:
                        result['products_found'] = products
        
        except Exception as e:
            print(f"Error checking inventory for {result['store_name']}: {e}")
        
        return result
    
    def _try_site_search(self, website: str) -> bool:
        """
        Attempt to use the site's search functionality.
        
        Args:
            website: The website URL
        
        Returns:
            True if search was attempted, False otherwise
        """
        try:
            # Common search input selectors
            search_selectors = [
                "input[type='search']",
                "input[name='q']",
                "input[name='search']",
                "input[placeholder*='search' i]",
                "input[class*='search' i]",
                "#search",
                ".search-input"
            ]
            
            for selector in search_selectors:
                try:
                    search_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    search_input.clear()
                    search_input.send_keys("Arkham Horror LCG")
                    search_input.submit()
                    return True
                except NoSuchElementException:
                    continue
        
        except Exception as e:
            print(f"Error trying site search: {e}")
        
        return False
    
    def _extract_products(self) -> List[str]:
        """
        Extract product names from the current page.
        
        Returns:
            List of product names found
        """
        products = []
        
        try:
            # Try to find product titles/names
            # This is generic and may need adjustment for specific sites
            product_selectors = [
                ".product-title",
                ".product-name",
                "h2.product",
                "h3.product",
                ".item-title"
            ]
            
            for selector in product_selectors:
                try:
                    product_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for elem in product_elements[:5]:  # Limit to 5 products
                        text = elem.text.strip()
                        if text and "arkham horror" in text.lower():
                            products.append(text)
                    
                    if products:
                        break
                except NoSuchElementException:
                    continue
        
        except Exception as e:
            print(f"Error extracting products: {e}")
        
        return products
    
    def scan_location(self, location: str) -> List[Dict[str, any]]:
        """
        Main method to scan a location for game stores with Arkham Horror products.
        
        Args:
            location: Location to search (e.g., "Seattle, WA")
        
        Returns:
            List of stores with their Arkham Horror inventory status
        """
        results = []
        
        try:
            self.setup_driver()
            
            print(f"Searching for game stores near: {location}")
            stores = self.search_game_stores(location)
            print(f"Found {len(stores)} game stores")
            
            for i, store in enumerate(stores, 1):
                print(f"\nChecking store {i}/{len(stores)}: {store.get('name', 'Unknown')}")
                inventory_result = self.check_store_inventory(store)
                results.append(inventory_result)
                
                # Small delay between stores
                time.sleep(1)
        
        finally:
            self.close_driver()
        
        return results


def format_results(results: List[Dict[str, any]]) -> str:
    """
    Format scan results into a readable string.
    
    Args:
        results: List of scan results
    
    Returns:
        Formatted string with results
    """
    output = []
    output.append("=" * 80)
    output.append("ARKHAM HORROR LCG STORE SCAN RESULTS")
    output.append("=" * 80)
    
    stores_with_products = [r for r in results if r['has_arkham_products']]
    
    output.append(f"\nTotal stores checked: {len(results)}")
    output.append(f"Stores with Arkham Horror products: {len(stores_with_products)}")
    output.append("\n" + "-" * 80)
    
    if stores_with_products:
        output.append("\nSTORES WITH ARKHAM HORROR LCG PRODUCTS:")
        output.append("-" * 80)
        
        for store in stores_with_products:
            output.append(f"\n🎲 {store['store_name']}")
            output.append(f"   Website: {store['website']}")
            output.append(f"   Phone: {store['phone']}")
            output.append(f"   Address: {store['address']}")
            output.append(f"   Google Maps: {store['maps_url']}")
            
            if store['products_found']:
                output.append(f"   Products found:")
                for product in store['products_found']:
                    output.append(f"      - {product}")
            else:
                output.append(f"   Note: Arkham Horror mentioned on site (specific products not listed)")
            output.append("")
    
    # List stores without products
    stores_without = [r for r in results if not r['has_arkham_products'] and r['search_attempted']]
    if stores_without:
        output.append("\n" + "-" * 80)
        output.append("STORES CHECKED (No Arkham Horror products found):")
        output.append("-" * 80)
        for store in stores_without:
            output.append(f"  • {store['store_name']}")
            if store['website'] != 'N/A':
                output.append(f"    Website: {store['website']}")
    
    # List stores without websites
    stores_no_website = [r for r in results if not r['search_attempted']]
    if stores_no_website:
        output.append("\n" + "-" * 80)
        output.append("STORES WITHOUT WEBSITES (Could not check inventory):")
        output.append("-" * 80)
        for store in stores_no_website:
            output.append(f"  • {store['store_name']}")
            output.append(f"    Phone: {store['phone']}")
            output.append(f"    Google Maps: {store['maps_url']}")
    
    output.append("\n" + "=" * 80)
    
    return "\n".join(output)


if __name__ == "__main__":
    # Example usage
    scanner = ArkhamHorrorStoreScanner(headless=True)
    
    # Get location from user
    location = input("Enter location to search (e.g., 'Seattle, WA' or '90210'): ")
    
    # Perform scan
    results = scanner.scan_location(location)
    
    # Display results
    print("\n")
    print(format_results(results))
