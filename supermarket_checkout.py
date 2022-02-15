# uvicorn supermarket_checkout:app --reload
from fastapi import FastAPI, Body
from typing import Optional
from pydantic import BaseModel


class NewPurchase(BaseModel):
    basket_id: int
    product_id: int
    quantity: Optional[int] = None


app = FastAPI()

products = {
    1: {"name": "Bread", "price": 10.0},
    2: {"name": "Chocolate", "price": 15.0},
    3: {"name": "Vodka", "price": 40.0},
}
baskets = {
    1: {
        "current_total": 0.0,
        "products": {},
    },
}

discounts = {
    1: {"quantity": 2, "new_price": 15.0},
    2: {"quantity": 4, "new_price": 40.0},
    3: {"quantity": 3, "new_price": 100.0},
}


@app.get("/")
def home():
    return {"Data": "test"}


@app.post("/create-basket")
def create_basket():
    last_id = list(baskets.keys())[-1]
    new_basket_id = last_id + 1
    baskets[new_basket_id] = {
        "current_total": 0.0,
        "products": {},
    }

    return {"new_basket_id": new_basket_id}


@app.get("/get-basket")
def get_basket(basket_id: int):
    return baskets.get(basket_id)


@app.get("/total-value-shopping-basket")
def get_total_value_shopping_basket(basket_id: int):
    return {"current_total": baskets.get(basket_id).get("current_total")}


@app.get("/basket-list-of-products")
def get_basket_list_of_products(basket_id: int):
    return {"products": baskets.get(basket_id).get("products")}


@app.post("/add-product-to-basket/")
async def add_product_to_basket(new_purchase: NewPurchase):
    new_purchase_dict = new_purchase.dict()
    product_id = new_purchase_dict.get("product_id")
    product = products.get(product_id)
    discount = discounts.get(product_id)
    basket = baskets.get(new_purchase_dict.get("basket_id"))

    quantity = new_purchase_dict.get("quantity", 1)
    discount_quantity = discount.get("quantity")

    if basket.get("products").get(product_id) is None:
        basket.get("products")[product_id] = {
            "name": product.get("name"),
            "quantity": quantity,
        }
    else:
        basket.get("products")[product_id]["quantity"] += quantity

    offers_to_apply = quantity // discount_quantity

    if offers_to_apply >= 1:
        basket["current_total"] += discount.get("new_price") * offers_to_apply
        quantity -= offers_to_apply * discount_quantity
    if quantity > 0:
        print("saaaaa")
        print(product.get("price") * quantity)
        basket["current_total"] += product.get("price") * quantity
    return basket
