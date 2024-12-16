import mysql.connector
from datetime import datetime

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mysq001"
)

cursor = db.cursor()


# View Menu
def view_Menu():
    cursor.execute("SELECT * FROM menu")
    menu = cursor.fetchall()

    print("\n               Pizza Menu:")
    #print("\nPizza_id  |  Pizza_Name  |  Pizza_Type  |  Size  | regular_price")

    for item in menu:
        print(f"\nPizza_id:{item[0]}  |  Pizza_Name:{item[1]}  |  Pizza_Type:{item[2]}  |  Size:{item[3]}  |  regular_price: ₹{item[4]}")


# View Toppings
def view_Topping():
    cursor.execute("SELECT * FROM topping")
    toppings = cursor.fetchall()

    print("\n               Toppings Menu:")

    for topping in toppings:
        print(f"\n Topping_id:{topping[0]}  | Topping_Name: {topping[1]}  |  topping_price: ₹{topping[2]}")


# Place order
def order(Pizza_id, Topping_id, Quantity, wants_topping):
    if wants_topping == "yes":
        # Fetch pizza and topping prices
        cursor.execute(f"SELECT regular_price FROM menu WHERE pizza_id = {Pizza_id}")
        pizza_price = cursor.fetchone()[0]

        cursor.execute(f"SELECT topping_price FROM topping WHERE topping_id = {Topping_id}")
        topping_price = cursor.fetchone()[0]

        total_price = (pizza_price + topping_price) * Quantity
    else:
        # If no topping is chosen, just get the pizza price
        cursor.execute(f"SELECT regular_price FROM menu WHERE pizza_id = {Pizza_id}")
        pizza_price = cursor.fetchone()[0]
        Topping_id = None  # No topping chosen
        total_price = pizza_price * Quantity

    
    order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insert order into the database
    s = "INSERT INTO `order details_pizza` (Pizza_id, Topping_id, Quantity, Total_Price, order_date) VALUES (%s, %s, %s, %s, %s)"
    v = (Pizza_id, Topping_id, Quantity, total_price, order_date)
    cursor.execute(s, v)
    db.commit()

    print(f"Order placed successfully! Total amount: ₹{total_price:.2f}")
    print(f"Order Date and Time: {order_date}")


# View placed orders
def displayplace_order():
    cursor.execute("SELECT * FROM `order details_pizza`")
    place_order = cursor.fetchall()

    print("\n               Placed Orders:")
    for order in place_order:
        print(f"\n Order details_id: {order[0]}  |  Pizza_id: {order[1]}  |  Topping_id: {order[2]}  |  Quantity: {order[3]}  |  Total_Price: ₹{order[4]}  |  order_date: {order[5]}")


# Main function
def main():
    while True:
        print("\n-- Welcome to the Pizza Ordering System --")
        print("\n Welcome To The JoJo Pizza Hub ")
        view_Menu()
        view_Topping()
        print("\n \n")
        print("1. Place Order")
        print("2. View Placed Orders")
        print("3. Exit")

        choice = int(input("\nEnter Your Choice: "))

        if choice == 1:
            pizza_id = int(input("Enter the Pizza ID you want to order: "))
            wants_topping = input("Do you want a topping? (yes/no): ").strip().lower()
            if wants_topping == "yes":
                topping_id = int(input("Enter the Topping ID you want to order: "))
            else:
                topping_id = None
            quantity = int(input("Enter the quantity: "))
            order(pizza_id, topping_id, quantity, wants_topping)

        elif choice == 2:
            displayplace_order()

        elif choice == 3:
            print("Thank you for using the Pizza Ordering System. ")
            print("Goodbye!")
            break

        else:
            print("Invalid choice! Please try again.")
            


if __name__ == "__main__":
    main()

cursor.close()
db.close()