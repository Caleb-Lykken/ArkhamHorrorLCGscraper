#!/usr/bin/env python3
"""
Example usage script for the Arkham Horror LCG Store Scraper.

This demonstrates how to use the scraper programmatically.
"""

from arkham_scraper import ArkhamHorrorStoreScanner, format_results


def main():
    """Run example scraper."""
    print("=" * 80)
    print("Arkham Horror LCG Store Scraper - Example")
    print("=" * 80)
    print()
    
    # Example 1: Basic usage
    print("Example 1: Search for stores in Seattle, WA")
    print("-" * 80)
    
    scanner = ArkhamHorrorStoreScanner(headless=True)
    results = scanner.scan_location("Seattle, WA")
    
    print(format_results(results))
    print()
    
    # Example 2: Search by ZIP code
    print("\nExample 2: Search for stores by ZIP code (90210)")
    print("-" * 80)
    
    scanner = ArkhamHorrorStoreScanner(headless=True)
    results = scanner.scan_location("90210")
    
    print(format_results(results))


if __name__ == "__main__":
    main()
