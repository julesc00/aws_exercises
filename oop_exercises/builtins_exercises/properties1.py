class Ninja:
    def __init__(self):
        self._score: int = 0

        @property
        def score(self):
            return self._score

        # manage how the `score` property is set
        @score.setter
        def score(self, new_value):
            if new_value < 0:
                raise ValueError("Score cannot be less than 0")
            self._score = new_value
