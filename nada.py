class Parrot:
    def __init__(self):
        self._voltage = 100000

    @property
    def voltage(self):
        """Get the current voltage."""
        return self._voltage


p = Parrot()
p._voltage = 20
print(p.voltage)
