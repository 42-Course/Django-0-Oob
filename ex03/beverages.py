#!/usr/bin/python3


class HotBeverage:
    """A generic hot beverage."""

    def __init__(self):
        self.price = 0.30
        self.name = "hot beverage"

    def description(self):
        return "Just some hot water in a cup."

    def __str__(self):
        return (
            "name : {}\n"
            "price : {:.2f}\n"
            "description : {}".format(
                self.name, self.price, self.description())
        )


class Coffee(HotBeverage):
    def __init__(self):
        super().__init__()
        self.name = "coffee"
        self.price = 0.40

    def description(self):
        return "A coffee, to stay awake."


class Tea(HotBeverage):
    def __init__(self):
        super().__init__()
        self.name = "tea"


class Chocolate(HotBeverage):
    def __init__(self):
        super().__init__()
        self.name = "chocolate"
        self.price = 0.50

    def description(self):
        return "Chocolate, sweet chocolate..."


class Cappuccino(HotBeverage):
    def __init__(self):
        super().__init__()
        self.name = "cappuccino"
        self.price = 0.45

    def description(self):
        return "Un po' di Italia nella sua tazza!"


if __name__ == '__main__':
    for beverage in (HotBeverage(), Coffee(), Tea(), Chocolate(),
                     Cappuccino()):
        print(beverage)
        print()
