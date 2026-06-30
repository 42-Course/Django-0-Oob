#!/usr/bin/python3


class Intern:
    """A cheap, nameless helper for your start-up."""

    class Coffee:
        def __str__(self):
            return "This is the worst coffee you ever tasted."

    def __init__(self, name="My name? I'm nobody, an intern, I have no name."):
        self.name = name

    def __str__(self):
        return self.name

    def work(self):
        raise Exception("I'm just an intern, I can't do that...")

    def make_coffee(self):
        return Intern.Coffee()


if __name__ == '__main__':
    nobody = Intern()
    mark = Intern("Mark")

    print(nobody)
    print(mark)

    print(mark.make_coffee())

    try:
        nobody.work()
    except Exception as e:
        print(e)
