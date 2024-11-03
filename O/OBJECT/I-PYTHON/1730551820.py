class Vehicle:
    def __init__(self, color, wheels):
            self.color = color
            self.wheels = wheels

class Car(Vehicle):
    def __init__(self, color, wheels, doors):
        super().__init__(color, wheels)
        self.doors = doors

    def honk(self):
        print("Honk!")

my_car = Car("red", 4, 4)
print(my_car.color, my_car.wheels,
my_car.doors)
my_car.honk()
