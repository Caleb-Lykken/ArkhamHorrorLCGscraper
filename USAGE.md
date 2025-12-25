# Usage Guide

## Quick Start

### Interactive Mode

The simplest way to use the scraper is in interactive mode:

```bash
python3 arkham_scraper.py
```

You'll be prompted to enter a location, such as:
- "Seattle, WA"
- "New York, NY"
- "90210" (ZIP code)
- "Portland, Oregon"

### Programmatic Usage

For integration into your own scripts:

```python
from arkham_scraper import ArkhamHorrorStoreScanner, format_results

# Create scanner
scanner = ArkhamHorrorStoreScanner(headless=True)

# Scan a location
results = scanner.scan_location("Chicago, IL")

# Format and display results
print(format_results(results))

# Access individual results
for result in results:
    if result['has_arkham_products']:
        print(f"Store: {result['store_name']}")
        print(f"Website: {result['website']}")
        print(f"Phone: {result['phone']}")
```

## Understanding Results

Each store result contains:

- **store_name**: Name of the game store
- **website**: Store's website URL (or 'N/A' if not available)
- **phone**: Phone number (or 'N/A' if not available)
- **address**: Physical address
- **maps_url**: Direct Google Maps link to the store
- **has_arkham_products**: Boolean - True if Arkham Horror products found
- **products_found**: List of specific products (when extractable)
- **search_attempted**: Boolean - True if website was checked

## Tips for Best Results

1. **Be Specific**: Use complete location names like "Seattle, Washington" instead of just "Seattle"

2. **Use ZIP Codes**: For smaller areas, ZIP codes often give better localized results

3. **Check Multiple Locations**: Run the scraper for nearby cities to find all options

4. **Manual Verification**: Always call stores to confirm product availability and pricing

5. **Run During Off-Hours**: Running the scraper late at night or early morning may be faster

## Troubleshooting

### Chrome Not Found
If you get an error about Chrome not being installed:
```bash
# Ubuntu/Debian
sudo apt-get install chromium-browser

# macOS
brew install --cask google-chrome
```

### Timeout Errors
If you experience timeout errors:
- Check your internet connection
- Try running with `headless=False` to see what's happening
- Increase wait times in the code if needed

### No Stores Found
If no stores are found:
- Try a different location format (city name vs ZIP code)
- Verify the location is correct
- Some areas may have limited board game stores

## Advanced Usage

### Custom Keywords

You can modify the Arkham Horror keywords by accessing the scanner object:

```python
scanner = ArkhamHorrorStoreScanner()
scanner.arkham_keywords.append("edge of the earth")
scanner.arkham_keywords.append("scarlet keys")
```

### Non-Headless Mode (Debugging)

To see the browser in action:

```python
scanner = ArkhamHorrorStoreScanner(headless=False)
results = scanner.scan_location("Your Location")
```

### Error Handling

```python
try:
    scanner = ArkhamHorrorStoreScanner()
    results = scanner.scan_location("Your Location")
    print(format_results(results))
except Exception as e:
    print(f"Error occurred: {e}")
```

## Examples

### Example 1: Search by City
```python
from arkham_scraper import ArkhamHorrorStoreScanner, format_results

scanner = ArkhamHorrorStoreScanner()
results = scanner.scan_location("Boston, MA")
print(format_results(results))
```

### Example 2: Search Multiple Locations
```python
from arkham_scraper import ArkhamHorrorStoreScanner, format_results

locations = ["Seattle, WA", "Portland, OR", "San Francisco, CA"]
scanner = ArkhamHorrorStoreScanner()

for location in locations:
    print(f"\n{'='*80}")
    print(f"Searching {location}")
    print('='*80)
    results = scanner.scan_location(location)
    print(format_results(results))
```

### Example 3: Filter Results
```python
from arkham_scraper import ArkhamHorrorStoreScanner

scanner = ArkhamHorrorStoreScanner()
results = scanner.scan_location("Denver, CO")

# Filter to only stores with products
stores_with_products = [r for r in results if r['has_arkham_products']]

print(f"Found {len(stores_with_products)} stores with Arkham Horror products:")
for store in stores_with_products:
    print(f"\n{store['store_name']}")
    print(f"  Call: {store['phone']}")
    print(f"  Visit: {store['website']}")
```

## Limitations

- **Rate Limiting**: Built-in delays respect websites; don't modify without care
- **Dynamic Content**: Some stores use JavaScript-heavy sites that may not load fully
- **Product Details**: Specific product availability may require manual verification
- **Regional Coverage**: Results depend on stores being listed on Google Maps
- **Website Changes**: Store website structures change over time

## Contributing

If you find ways to improve the scraper, particularly for specific store chains or regions, please contribute!
