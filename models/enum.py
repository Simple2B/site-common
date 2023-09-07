import enum


class Languages(enum.Enum):
    ENGLISH = "en"
    GERMANY = "de"

    def __str__(self):
        return self.name.capitalize()
