from enum import Enum


# Define an enumeration for product categories
class Category(Enum):
    SMART_PHONES = "Smart Phones"
    LAPTOPS = "Laptops"
    IPHONES = "iPhones"


# Define an enumeration for inventory statuses
class InventoryStatus(Enum):
    AVAILABLE = "Available"
    OUT_OF_STOCK = "Out of Stock"
    IN_TRANSIT = "In Transit"
    DAMAGED = "Damaged"
    RESERVED = "Reserved"
    DISCONTINUED = "Discontinued"
    LOW = "Low"