#!/usr/bin/env python3
"""
Test script to verify the scraper functionality without running a full scan.
"""

from arkham_scraper import ArkhamHorrorStoreScanner, format_results


def test_scanner_initialization():
    """Test that the scanner can be initialized."""
    print("Testing scanner initialization...")
    
    # Test headless mode
    scanner = ArkhamHorrorStoreScanner(headless=True)
    assert scanner.headless == True
    assert scanner.driver is None
    print("✓ Headless scanner initialized successfully")
    
    # Test non-headless mode
    scanner = ArkhamHorrorStoreScanner(headless=False)
    assert scanner.headless == False
    print("✓ Non-headless scanner initialized successfully")


def test_arkham_keywords():
    """Test that Arkham Horror keywords are defined."""
    print("\nTesting Arkham Horror keywords...")
    
    scanner = ArkhamHorrorStoreScanner()
    assert len(scanner.arkham_keywords) > 0
    assert "arkham horror" in scanner.arkham_keywords
    print(f"✓ Found {len(scanner.arkham_keywords)} Arkham Horror keywords")
    for keyword in scanner.arkham_keywords:
        print(f"  - {keyword}")


def test_format_results():
    """Test result formatting."""
    print("\nTesting result formatting...")
    
    # Test with empty results
    empty_results = []
    output = format_results(empty_results)
    assert "ARKHAM HORROR LCG STORE SCAN RESULTS" in output
    assert "Total stores checked: 0" in output
    print("✓ Empty results formatted correctly")
    
    # Test with mock results
    mock_results = [
        {
            'store_name': 'Test Game Store',
            'website': 'https://example.com',
            'phone': '+1-555-0123',
            'address': '123 Test St',
            'maps_url': 'https://maps.google.com/test',
            'has_arkham_products': True,
            'products_found': ['Arkham Horror Core Set'],
            'search_attempted': True
        },
        {
            'store_name': 'Another Store',
            'website': 'N/A',
            'phone': '+1-555-0456',
            'address': '456 Main Ave',
            'maps_url': 'https://maps.google.com/test2',
            'has_arkham_products': False,
            'products_found': [],
            'search_attempted': False
        }
    ]
    
    output = format_results(mock_results)
    assert "Total stores checked: 2" in output
    assert "Stores with Arkham Horror products: 1" in output
    assert "Test Game Store" in output
    assert "Arkham Horror Core Set" in output
    print("✓ Mock results formatted correctly")


def test_store_info_structure():
    """Test that check_store_inventory returns proper structure."""
    print("\nTesting store info structure...")
    
    scanner = ArkhamHorrorStoreScanner()
    
    # Test with minimal store info
    store_info = {
        'name': 'Test Store',
        'website': '',
        'phone': '',
        'address': '',
        'maps_url': ''
    }
    
    result = scanner.check_store_inventory(store_info)
    
    # Verify all expected keys are present
    expected_keys = [
        'store_name', 'website', 'phone', 'address', 'maps_url',
        'has_arkham_products', 'products_found', 'search_attempted'
    ]
    
    for key in expected_keys:
        assert key in result, f"Missing key: {key}"
    
    print("✓ Store info structure is correct")
    print(f"  Keys: {', '.join(expected_keys)}")


def main():
    """Run all tests."""
    print("=" * 80)
    print("Arkham Horror LCG Store Scraper - Unit Tests")
    print("=" * 80)
    print()
    
    try:
        test_scanner_initialization()
        test_arkham_keywords()
        test_format_results()
        test_store_info_structure()
        
        print("\n" + "=" * 80)
        print("✓ All tests passed!")
        print("=" * 80)
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
