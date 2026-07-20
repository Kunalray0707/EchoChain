"""
Test fixture functions for unit tests
"""

def sample_bom_data():
    return [
        {
            "SKU": "SKU-TEST-001",
            "Product": "Test Smartphone Pro",
            "Manufacturer": "TestCorp",
            "Category": "Smartphones",
            "Component": "Lithium Battery",
            "Manufacturing Cost": 45.0,
            "Production Date": "2023-01-01",
            "Country": "United States",
            "Supplier": "Foxconn",
            "Carbon Footprint": 12.5,
            "Weight": 150.0,
            "Material": "Lithium",
            "Warranty Period": 12,
            "Warranty Claims": 10,
            "Failure Rate": 0.02
        }
    ]

def sample_listing_item():
    return {
        "listing_id": "LIST-EBA-10001",
        "marketplace": "eBay",
        "product_title": "Apple iPhone 14 Pro 256GB Space Black",
        "condition": "Refurbished - Grade A",
        "price": 500.0,
        "currency": "EUR",
        "location": "Berlin, Germany",
        "seller_rating": 4.9,
        "sold_count": 10,
        "listing_date": "2024-01-10",
        "shipping_cost": 5.0,
        "images_count": 4,
        "description": "Clean refurbished phone."
    }
