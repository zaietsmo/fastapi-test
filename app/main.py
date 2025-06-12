import json
import os
import time
from typing import List, Optional

from fastapi import FastAPI, HTTPException

from app.schemas.product import Product

app = FastAPI()

DATA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "scraper", "output", "products.json"
)


def load_products() -> List[Product]:
    try:
        with open(DATA_PATH, encoding="utf-8") as f:
            data = json.load(f)
        return [Product(**item) for item in data]
    except Exception as e:
        return []


@app.get("/all_products/", response_model=List[Product])
def get_all_products():
    products = load_products()
    return products


@app.get("/products/{product_name}", response_model=Optional[Product])
def get_product(product_name: str):
    products = load_products()
    for product in products:
        if product.name and product.name.lower() == product_name.lower():
            return product
    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/products/{product_name}/{product_field}")
def get_product_field(product_name: str, product_field: str):
    products = load_products()
    for product in products:
        if product.name and product.name.lower() == product_name.lower():
            value = getattr(product, product_field, None)
            if value is not None:
                return {product_field: value}
            else:
                raise HTTPException(status_code=404, detail="Field not found")
    raise HTTPException(status_code=404, detail="Product not found")


