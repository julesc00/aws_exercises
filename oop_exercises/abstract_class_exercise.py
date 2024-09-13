from abc import ABC, abstractmethod


"""
An abstract class in Python is a class that cannot be instantiated directly and is used to 
define a common interface for other subclasses. It serves as a blueprint for concrete classes, 
enforcing that certain methods must be implemented by any subclass. This is useful for 
creating a structured hierarchy where subclasses must implement specific behaviors.

Python provides the abc (Abstract Base Class) module to define abstract classes. Within an 
abstract class, methods can be declared abstract using the @abstractmethod decorator. 
These methods do not contain any implementation in the abstract class, and subclasses must 
provide their own implementation for these methods.
"""


# Abstract class
class Animal(ABC):
    @abstractmethod
    def sound(self):
        pass


class Dog(Animal):
    def sound(self):
        return "Bark"


class Cat(Animal):
    def sound(self):
        return "Meow"

if __name__ == "__main__":
    dog = Dog()
    print(dog.sound())
