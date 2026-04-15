import json
from pathlib import Path

FILE_PATH = Path("src/products/products.json")

def read_products():
    if not FILE_PATH.exists():
        return []
    with open(FILE_PATH, "r") as file:
        return json.load(file)

def write_products(products):
    with open(FILE_PATH, "w") as file:
        json.dump(products, file, indent=4)