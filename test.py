# print("Welcome to burger store")

# def price_coffee(size):
#     if size == "S":
#         price1 = 40
#     elif size == "M":
#         price1 = 50
#     elif size == "L":
#         price1 = 60
#     return price1

# def price_ham(size):
#     if size == "S":
#         price2 = 100
#     elif size == "M":
#         price2 = 150
#     elif size == "L":
#         price2 = 200
#     return price2

# type = input("(b)urgur or (c)coffee: ")
# if type == "c":
#     size = input("What size (S,M,L): ")
#     price1 = price_coffee(size)
#     mi = input("milk y/n: ")
#     if mi == "y":
#         price1 += 10
#         print(f"Coffee with milk {size} {price1} baht")
#     if mi == "n":
#         print(f"Coffee {size} {price1} baht")
# elif type == "b":
#     size = input("What size (S,M,L): ")
#     price2 = price_ham(size)
#     meat = input("What meat (c)hicken,(p)ork: ")
#     if meat == "c":
#         a = "Chicken"
#     elif meat == "p":
#         a = "Pork"
#     veg = input("Vegetable y/n: ")
#     if veg == "y":
#         print(f"{a} burgur {size} with vegetable {price2} baht")
#     if veg == "n":
#         print(f"{a} burgur {size} no vegetable {price2} baht")   
# print("Thank you") 


# area = ??
# circum =?? 

# weakend adult 200 chid = 100
# m- th = adult 150 chid = 50
# มามากกว่า 10 คน ลด  20 %



day = input("weakend")
adult = int(input("How many"))
chid = int(input("How many"))

if day == "y":
    price = adult*200+chid*100
else:
    price = adult*150+chid*50

if (adult+chid) >= 10 :
    price = price*0.8

print(f"price: {price:.2f}")

    







