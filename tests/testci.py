def to_absolute(number):
    if number <= 0:
        return -number
    return number

def test_to_absolute_positive():
    assert to_absolute(3) == 3

def test_to_absolute_negative():
    assert to_absolute(-10) == 10

def test_to_absolute_zero():
    assert to_absolute(0) == 0