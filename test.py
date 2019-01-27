class Car:

    @classmethod
    def afunction(cls):
        print(cls.bfunction())

    @staticmethod
    def bfunction():
        return "I'm B"

Car.afunction()