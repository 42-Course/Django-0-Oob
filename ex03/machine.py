#!/usr/bin/python3
import random

from beverages import HotBeverage, Coffee, Tea, Chocolate, Cappuccino


class CoffeeMachine:
    """A cheap coffee machine that breaks down every 10 drinks."""

    class EmptyCup(HotBeverage):
        def __init__(self):
            super().__init__()
            self.name = "empty cup"
            self.price = 0.90

        def description(self):
            return "An empty cup?! Gimme my money back!"

    class BrokenMachineException(Exception):
        def __init__(self):
            super().__init__("This coffee machine has to be repaired.")

    def __init__(self):
        self.broken = False
        self.served = 0

    def repair(self):
        self.broken = False
        self.served = 0

    def serve(self, beverage_class):
        if self.broken:
            raise CoffeeMachine.BrokenMachineException()
        self.served += 1
        if self.served >= 10:
            self.broken = True
        if random.choice([True, False]):
            return beverage_class()
        return CoffeeMachine.EmptyCup()


if __name__ == '__main__':
    machine = CoffeeMachine()
    drinks = [Coffee, Tea, Chocolate, Cappuccino]

    for _ in range(2):
        try:
            while True:
                print(machine.serve(random.choice(drinks)))
                print('---')
        except CoffeeMachine.BrokenMachineException as e:
            print(e)
            print("Repairing the machine...")
            machine.repair()
