"""
EchoChain PySpark Pipeline Configuration & Schemas
"""

from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType, IntegerType, FloatType, DateType
)

# Currency exchange rates to USD
CURRENCY_CONVERSION = {
    "USD": 1.0,
    "EUR": 1.09,
    "GBP": 1.27,
    "BRL": 0.18,
    "INR": 0.012
}

# Condition normalization dictionary
CONDITION_MAPPING = {
    "New - Open Box": "Like New",
    "Refurbished - Grade A": "Refurbished",
    "Used - Excellent": "Excellent",
    "Used - Good": "Good",
    "Used - Fair": "Fair",
    "For Parts / Non-Functional": "Salvage"
}

# Schemas
BOM_SCHEMA = StructType([
    StructField("SKU", StringType(), True),
    StructField("Product", StringType(), True),
    StructField("Manufacturer", StringType(), True),
    StructField("Category", StringType(), True),
    StructField("Component", StringType(), True),
    StructField("Manufacturing Cost", DoubleType(), True),
    StructField("Production Date", StringType(), True),
    StructField("Country", StringType(), True),
    StructField("Supplier", StringType(), True),
    StructField("Carbon Footprint", DoubleType(), True),
    StructField("Weight", DoubleType(), True),
    StructField("Material", StringType(), True),
    StructField("Warranty Period", IntegerType(), True),
    StructField("Warranty Claims", IntegerType(), True),
    StructField("Failure Rate", DoubleType(), True)
])

WARRANTY_SCHEMA = StructType([
    StructField("Customer ID", StringType(), True),
    StructField("SKU", StringType(), True),
    StructField("Issue", StringType(), True),
    StructField("Failure Component", StringType(), True),
    StructField("Claim Date", StringType(), True),
    StructField("Resolution", StringType(), True),
    StructField("Repair Cost", DoubleType(), True)
])

LISTING_SCHEMA = StructType([
    StructField("listing_id", StringType(), True),
    StructField("marketplace", StringType(), True),
    StructField("product_title", StringType(), True),
    StructField("condition", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("currency", StringType(), True),
    StructField("location", StringType(), True),
    StructField("seller_rating", DoubleType(), True),
    StructField("sold_count", IntegerType(), True),
    StructField("listing_date", StringType(), True),
    StructField("shipping_cost", DoubleType(), True),
    StructField("images_count", IntegerType(), True),
    StructField("description", StringType(), True)
])
