import sqlite3
import random

accounts = {}
account = ''


def create_an_account():
    card_MII = '400000'
    pin = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
    for i in range(9):
        card_MII += str(random.randint(0, 9))
    check_sum = str(luhn_algorithm(card_MII))
    card_MII += check_sum
    print('''Your card has been created
Your card number:''')
    print(card_MII)
    print('Your card PIN:')
    print(pin)
    cur.execute(f'INSERT INTO card(number, pin) VALUES ({card_MII}, {pin});')
    conn.commit()
    accounts[card_MII] = str(pin)


def log_into_account():
    global stop, account
    card_n = input('Enter your card number:\n> ')
    pin = input('Enter your pin:\n> ')
    cur.execute(f'SELECT number, pin FROM card;')
    zz = cur.fetchall()
    for num in zz:
        if card_n in num[0]:
            if pin == num[1]:
                account = card_n
                print('You have successfully logged in!')
                return True
            else:
                print('Wrong card number or PIN!')
                return
    print('Wrong card number or PIN!')


def transfer():
    global account
    tr_card = input('Transfer\nEnter card number:\n> ')
    lst_card = [int(x) for x in tr_card[:-1]]
    odd_list = []
    for ind, num in enumerate(lst_card):
        if ind % 2 == 0:
            z = num * 2
            if z > 9:
                odd_list.append(z - 9)
            else:
                odd_list.append(z)
        else:
            odd_list.append(num)
    summ = sum(odd_list)
    summ_a = summ
    while summ_a % 10 != 0:
        summ_a += 1
    check_n = summ_a - summ
    #print('Checking system', check_n, tr_card[-1])
    if str(check_n) == tr_card[-1]:
        cur.execute(f'SELECT number, balance FROM card;')
        zz = cur.fetchall()
        for kk in zz:
            if tr_card in kk[0]:
                money = input('Enter how much money you want to transfer:\n> ')
                #print(kk[1])
                for acc in zz:
                    if account in acc[0]:
                        if int(money) <= acc[1]:
                            cur.execute(f'UPDATE card SET balance = balance + {int(money)} WHERE number = {tr_card};')
                            cur.execute(f'UPDATE card SET balance = balance - {int(money)} WHERE number = {account};')
                            conn.commit()
                            print('Success!\n')
                            return
                        else:
                            print('Not enough money!')
                            return
        print('Such a card does not exist.')
    else:
        print('Probably you made mistake in the card number. Please try again!\n')


def account_in_operations():
    global stop, account
    while True:
        print('''1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit''')
        operation = input()
        if operation == '1':
            cur.execute(f'SELECT number, balance FROM card;')
            zz = cur.fetchall()
            for num in zz:
                if account in num[0]:
                    print(f'Balance {num[1]}')
        elif operation == '2':
            deposit = int(input('Enter income:\n> '))
            #print(deposit, account)
            #print(f'UPDATE card SET balance = {deposit} WHERE number = {account};')
            cur.execute(f'UPDATE card SET balance = balance + {deposit} WHERE number = {account};')
            conn.commit()
        elif operation == '3':
            transfer()
        elif operation == '4':
            cur.execute(f'SELECT number, balance FROM card;')
            zz = cur.fetchall()
            for num in zz:
                if account in num[0]:
                    cur.execute(f'DELETE FROM card WHERE number = {account};')
                    conn.commit()
        elif operation == '5':
            print('You have successfully logged out!')
            return True
        elif operation == '0':
            return False


def luhn_algorithm(card_m):
    lst_card = [int(x) for x in card_m]
    odd_list = []
    for ind, num in enumerate(lst_card):
        if ind % 2 == 0:
            z = num * 2
            if z > 9:
                odd_list.append(z - 9)
            else:
                odd_list.append(z)
        else:
            odd_list.append(num)
    summ = sum(odd_list)
    summ_a = summ
    while summ_a % 10 != 0:
        summ_a += 1
    return summ_a - summ


if __name__ == '__main__':
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    try:
        #cur.execute('DROP TABLE card')
        cur.execute('''CREATE TABLE card(
        id INTEGER, 
        number TEXT, 
        pin TEXT, 
        balance INTEGER DEFAULT 0
        );''')
        conn.commit()
    except sqlite3.OperationalError:
        pass
    stop = True
    while stop:
        print(
            '''1. Create an account
2. Log into account
0. Exit''')
        key = input('> ')
        if key == '1':
            create_an_account()
        elif key == '2':
            if log_into_account():
                stop = account_in_operations()
        elif key == '0':
            print('Bye!')
            stop = False
