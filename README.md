# supermarket_checkout_FastAPISupermarket Checkout

Think of a supermarket or grocery store where you do your shopping. You need to implement a checkout component responsible for total price calculation.
Requirements

1. Design and implement a supermarket checkout component with a readable API that calculates the total value of all products in a shopping basket.
2. Goods are priced individually and the component should:
   1. scan items one by one,
   2. give the ability to retrieve the actual price after each scan.
3. Goods can be sold at a reduced price, thus we need a concept of a discount. In particular, if you buy a specific amount of the product, the total price will be reduced (e.g. buy 3 bottles of vodka and you will pay less for each one).   
   Item Price Reduced Price
   Bread 10 2 for 15
   Chocolate 15 4 for 40
   Vodka 40 3 for 100
   Hints

- Talk when you type so all interviewers have a chance to follow your thinking
- Clean code and supple design play a vital role in the working solution

- Calculate total value in a shopping basket
- scan items one by one
- Get total price after each scan
-

1 total_value_shopping_basket, get, float:
list_items 
Sum all prices of the items in the list 2. Post (id)
Search for the item in the db and get the price
Add the item to a list
Total_value_shopping_basket 3. Calculate discount(id, amount)
Check if there is any discount
Return total price
