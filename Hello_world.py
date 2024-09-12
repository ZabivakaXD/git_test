import random

while True:
    varibal = int(input("Угадайте число от 1 до 10: "))
    random_number = random.randint(1, 10)
    if random_number == varibal:
        print("Поздравляю вы угадали")
        break
    else:
        print("Попробуйте ещё раз, число было", random_number)