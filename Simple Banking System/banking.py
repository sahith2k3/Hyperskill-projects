import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

try:
    cur.execute(f'''SELECT id FROM card;''')
except sqlite3.OperationalError:
    cur.execute('CREATE TABLE card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
    cur.execute('INSERT INTO card (id) values(1);')
    conn.commit()


def prompts_main():
    while True:
        print('''1. Create an account
2. Log into account
0. Exit''')
        p1 = int(input())
        if p1 == 1:
            p11()
        elif p1 == 2:
            p12()
        elif p1 == 0:
            print('\nBye!')
            exit()
        else:
            print("\nInvalid input, pls retry!\n")


def prompts_dash():
    print('''
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit''')
    p2 = int(input())
    while True:
        if p2 == 1:
            p21()
        elif p2 == 2:
            p22()
        elif p2 == 3:
            p23()
        elif p2 == 4:
            p24()
        elif p2 == 5:
            print("\nYou have successfully logged out!\n")
            return prompts_main()
        elif p2 == 0:
            print('\nBye!')
            exit()
        else:
            print("\nInvalid input, pls retry!\n")


def p11():
    print('''
Your card has been created
Your card number:''')
    new_card = str(400000)
    new_rand9 = str(random.randrange(1000000000)).rjust(9, '0')
    new_card += new_rand9
    new_card += str(luhn(new_card))
    print(new_card)
    new_pin = str(random.randrange(1, 9))*4
    print("Your card PIN:")
    print(new_pin)
    print()
    cur.execute('SELECT COUNT(*) FROM card')
    id = int(str(cur.fetchone())[1:-2]) + 1
    query = f"INSERT INTO card(id, number, pin) values({id}, '{new_card}', '{new_pin}');"
    cur.execute(query)
    conn.commit()


def p12():
    card_num = str(input("\nEnter your card number:\n"))
    card_pin = str(input("Enter your PIN:\n"))
    cur.execute(F"SELECT number,pin from card WHERE number = '{card_num}' AND pin = '{card_pin}';")
    response = str(cur.fetchone())[0]
    if not response == 'N':
        print("\nYou have successfully logged in!")
        global temp_login
        temp_login = card_num
        prompts_dash()
    else:
        print("\nWrong card number or PIN!\n")


def p21():
    cur.execute(f"SELECT balance FROM card where number = '{temp_login}';")
    balance = int(str(cur.fetchone())[1:-2])
    print('\nBalance:', balance)
    prompts_dash()


def p22():
    print("\nEnter income:")
    inc = int(input())
    cur.execute(f"UPDATE card set balance = balance + {inc} WHERE number = '{temp_login}';")
    conn.commit()
    print("Income was added!")
    prompts_dash()


def p23():
    print('''
Transfer
Enter card number:''')
    temp_tran = str(input())
    luhn_check = temp_tran[:-1]
    if luhn(luhn_check) == int(temp_tran[-1]):
        cur.execute(F"SELECT number from card WHERE number = '{temp_tran}';")
        response = str(cur.fetchone())[0]
        if not response == 'N':
            money_tran = int(input("Enter how much money you want to transfer:\n"))
            cur.execute(f"SELECT balance FROM card where number = '{temp_login}';")
            balance = int(str(cur.fetchone())[1:-2])
            if balance >= money_tran:
                cur.execute(f"UPDATE card set balance = balance - {money_tran} WHERE number = '{temp_login}'")
                cur.execute(f"UPDATE card set balance = balance + {money_tran} WHERE number = '{temp_tran}'")
                conn.commit()
                print("Success!")
                prompts_dash()
            else:
                print("Not enough money!")
                prompts_dash()
        else:
            print("Such a card does not exist.")
            prompts_dash()
    else:
        print("Probably you made a mistake in the card number. Please try again!")
        prompts_dash()


def p24():
    cur.execute(f"DELETE FROM card WHERE number = '{temp_login}';")
    conn.commit()
    print('The account has been closed!')
    prompts_main()


def luhn(x):
    result = 0
    for i in range(len(x)):
        if (i+1) % 2 != 0:
            n = 2*int(x[i])
            if n > 9:
                n -= 9
        else:
            n = int(x[i])
        result += n
    if (result % 10) == 0:
        return 0
    else:
        return 10 - (result % 10)


if __name__ == '__main__':
    temp_login = 0
    prompts_main()
