# Arkham Horror LCG Store Scraper

A web scraper that helps you find game stores in your area that carry Arkham Horror: The Card Game (LCG) products. The scraper searches for board game stores near your specified location, visits their websites, and checks if they have Arkham Horror LCG products in stock.

## Features

- 🔍 **Location-based search**: Search for game stores near any location (city, state, or ZIP code)
- 🎲 **Automated inventory checking**: Automatically visits store websites to check for Arkham Horror LCG products
- 📊 **Comprehensive results**: Returns store name, website, phone number, address, and available products
- 🤖 **Selenium-powered**: Uses Selenium WebDriver for reliable web scraping
- 🗺️ **Google Maps integration**: Finds stores using Google Maps search

## Requirements

- Python 3.7+
- Chrome browser installed
- Internet connection

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Caleb-Lykken/ArkhamHorrorLCGscraper.git
cd ArkhamHorrorLCGscraper
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

The script will automatically download the appropriate ChromeDriver for your system.

## Usage

### Basic Usage

Run the scraper interactively:

```bash
python arkham_scraper.py
```

You'll be prompted to enter a location (e.g., "Seattle, WA" or "90210"), and the scraper will:
1. Search for game stores in that area
2. Visit each store's website
3. Check for Arkham Horror LCG products
4. Display results with contact information and inventory status

### Programmatic Usage

You can also use the scraper in your own Python code:

```python
from arkham_scraper import ArkhamHorrorStoreScanner, format_results

# Create scanner instance
scanner = ArkhamHorrorStoreScanner(headless=True)

# Scan a location
results = scanner.scan_location("Portland, OR")

# Display formatted results
print(format_results(results))
```

### Configuration Options

```python
# Run with visible browser (useful for debugging)
scanner = ArkhamHorrorStoreScanner(headless=False)

# Scan results include:
# - store_name: Name of the game store
# - website: Store's website URL
# - phone: Store's phone number
# - address: Store's physical address
# - maps_url: Google Maps link to the store
# - has_arkham_products: Boolean indicating if Arkham Horror products were found
# - products_found: List of specific products found (if available)
```

## How It Works

1. **Store Discovery**: Uses Google Maps to search for "board game stores" near your specified location
2. **Information Extraction**: Extracts store name, phone number, website, and address from Google Maps
3. **Inventory Check**: Visits each store's website and searches for Arkham Horror LCG products
4. **Results Compilation**: Organizes all findings into a structured format

## Output Example

```
================================================================================
ARKHAM HORROR LCG STORE SCAN RESULTS
================================================================================

Total stores checked: 10
Stores with Arkham Horror products: 3

--------------------------------------------------------------------------------

STORES WITH ARKHAM HORROR LCG PRODUCTS:
--------------------------------------------------------------------------------

🎲 Fantasy Games Store
   Website: https://example-gamestore.com
   Phone: +1-555-0123
   Address: 123 Main St, Seattle, WA 98101
   Google Maps: https://maps.google.com/...
   Products found:
      - Arkham Horror: The Card Game Core Set
      - The Dunwich Legacy Expansion

🎲 Board Game Cafe
   Website: https://example-cafe.com
   Phone: +1-555-0456
   Address: 456 Pike St, Seattle, WA 98101
   Google Maps: https://maps.google.com/...
   Note: Arkham Horror mentioned on site (specific products not listed)

--------------------------------------------------------------------------------
```

## Limitations

- Results depend on store websites being accessible and searchable
- Some stores may require manual verification
- Product availability information may not be real-time
- Google Maps structure may change, affecting store discovery
- Rate limiting: The scraper includes delays to be respectful of websites

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is for personal use to help find Arkham Horror LCG products. Please be respectful of website terms of service and rate limits. The accuracy of results depends on store website structure and may require manual verification.

## License

MIT License - feel free to use and modify as needed.

## About Arkham Horror LCG

Arkham Horror: The Card Game is a Living Card Game (LCG) by Fantasy Flight Games set in the universe of H.P. Lovecraft's Cthulhu Mythos. While some products are out of print, many stores still carry inventory or can special order items.
