class CompassDirection:
    ordinal = -1


class North(CompassDirection):
    ordinal = 0


class South(CompassDirection):
    ordinal = 1


class West(CompassDirection):
    ordinal = 2


class East(CompassDirection):
    ordinal = 3


if __name__ == '__main__':
    print(f"Greetings from Compass!")
    for d in [North, South, West, East]:
        print(f"{d.__name__} ord:{d.ordinal}")

# END
