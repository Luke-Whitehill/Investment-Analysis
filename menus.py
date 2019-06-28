border = '-' * 20


def menus():
    print(border + 'MENU' + border)
    print('1. Risk/Return of Individual Asset')
    print('2. Efficient Frontier')
    print('3. Capital Asset Pricing Model')
    print('4. Recent High/Low Open/Close')
    print(border*2+'----')


menu = True
while menu:
    menus()
    key = int(input('Input your choice; '))

    if key == 1:
        import module1

    elif key == 2:
        import module2

    elif key == 3:
        print('Hello 3')
    elif key == 4:
        import module4
    else:
        print('Input invalid try again.')
