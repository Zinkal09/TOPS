fruit_stock={}

def add_fruitstock():
    fruit=input("Enter the fruit name:")
    qty=int(input("Enter the qty:"))
    price=int(input("Enter the Price:"))


    if fruit in fruit_stock:
        fruit_stock[fruit]['qut']+=qut
        fruit_stock[fruit]['price']+=price
    else:
         fruit_stock[fruit] = {'qty':qty , 'price':price}

def view_fruitstock():
    if fruit_stock:
        print("Current Stock")
        print(fruit_stock)
    else:
        print("stock is empty")


def update_fruitstock():
    fruit = input("Enter fruit name for update : ")
    if fruit in fruit_stock:
        qty=int(input("Enter the  new qty:"))
        price=int(input("Enter the  new Price:"))
        fruit_stock[fruit]={'qty':qty , 'price':price}
        print("stock update")
    else:
        print("fruit is not in stock")
        
