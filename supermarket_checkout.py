import os
from fastapi import FastAPI, Body, status
from fastapi.responses import RedirectResponse
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
    return RedirectResponse("/get-all-baskets", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/create-basket", status_code=status.HTTP_201_CREATED)
def create_basket():
    last_id = list(baskets.keys())[-1]
    new_basket_id = last_id + 1
    baskets[new_basket_id] = {
        "current_total": 0.0,
        "products": {},
    }

    return {"new_basket_id": new_basket_id}


@app.get("/get-basket", status_code=status.HTTP_200_OK)
def get_basket(basket_id: int):
    return baskets.get(basket_id)


@app.get("/get-all-baskets", status_code=status.HTTP_200_OK)
def get_basket():
    return baskets


@app.get("/total-value-shopping-basket", status_code=status.HTTP_200_OK)
def get_total_value_shopping_basket(basket_id: int):
    return {"current_total": baskets.get(basket_id).get("current_total")}


@app.get("/basket-list-of-products", status_code=status.HTTP_200_OK)
def get_basket_list_of_products(basket_id: int):
    return {"products": baskets.get(basket_id).get("products")}


@app.post("/add-product-to-basket/", status_code=status.HTTP_200_OK)
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

    discounts_to_apply = quantity // discount_quantity

    if discounts_to_apply > 0:
        basket["current_total"] += discount.get("new_price") * discounts_to_apply
        quantity -= discounts_to_apply * discount_quantity
    if quantity > 0:
        basket["current_total"] += product.get("price") * quantity
    return basket


if __name__ == "__main__":
    os.system("uvicorn supermarket_checkout:app --reload")
