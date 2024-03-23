GUESTS = (
    ("Compadre Chava", 4),
    ("Oscar gym", 2),
    ("Rebeca", 2),
    ("Oscar cuñado", 4),
    ("Juan Pablo", 4),
    ("Beni", 2),
    ("Don Beni y Nina", 2),
    ("Mi familia", 10),
    ("Cristian cuñado", 3),
    ("Pati", 3),
    ("Jaime", 3),
    ("Gerus", 2),
    ("Carlitos", 2),
    ("Flavio", 2),
    ("Angel", 2),
    ("Ezequiel", 2),
    ("Vero gym", 2),
    ("Bufa", 4),
    ("Maman", 2),
    ("Hector", 4),
    ("Alex", 4),
    ("Robert", 1),
    ("Efren", 5),
    ("Padre", 2),
    ("Lupita gym", 4),
    ("Mariana gym", 1),
    ("Silvia", 2),
    ("Denisse", 3),
    ("Alvaro", 1),
    ("Raul gym", 3),
    ("Uriel", 1),
)


def count_guests(guests):
    total_guests = sum(guest[1] for guest in guests)
    return f"The total number of guests is {total_guests}."


if __name__ == "__main__":
    print(count_guests(GUESTS))
