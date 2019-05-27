import calc

def test_add():
    if calc.add(1, 2) == 3:
        print('TRUE')
    else:
        print('FALSE')


def test_sub():
    if calc.sub(4, 2) == 2:
        print('TRUE')
    else:
        print('FALSE')


def test_mul():
    if calc.mul(5, 2) == 10:
        print('TRUE')
    else:
        print('FALSE')


def test_div():
    if calc.div(8, 2) == 4:
        print('TRUE')
    else:
        print('FALSE')

test_add()
test_sub()
test_mul()
test_div()