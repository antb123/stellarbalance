import requests
from decimal import *
from config import *
import sys


# print each transations
def print_transactions(x, p):

    # color = lambda GREEN, RED: GREEN if (x['to'] == ACCOUNT_ID) else RED
    if p == 1:
        if x['to'] == ACCOUNT_ID:
            color = GREEN
        else :
            color = RED
        print(color + x['created_at'], x['amount'], x['asset_code'], x['to'] + EOC)
    return(0)

# print balance accounts
def print_balance_accounts(lst):

    for i in range(len(lst[0])):
        print(lst[0][i], '\t:', lst[1][i])
    return(1)

# add new currency at the list and its balance to 0.
def list_new(lst, add):

    lst[0].append(add)
    lst[1].append(0)
    return(lst)

# add or subtract according to the situation.
def update_balance(lst, index, data):

    if data['to'] == ACCOUNT_ID:
        lst[1][index] = (Decimal(lst[1][index]) + Decimal(data['amount']))
    else:
        lst[1][index] = (Decimal(lst[1][index]) - Decimal(data['amount']))
    return(lst)

# search currency match, append a new if no found and call update_balance().
def match_currency(lst, asset_code, data):

    found = False
    n = 0

    for i in range(len(lst[0])):
        if lst[0][i] == asset_code :
            n = i
            found = True
    if found == False :
        lst = list_new(lst, asset_code)
        n = (len(lst[0]) - 1)# why $n is out of range in update_balance
    lst = update_balance(lst, n, data)
    return(lst)

def is_again(x, stop, again):

    if (x['created_at'] > stop):
        again = False
    return(again)

################################## main #######################################

# color code
GREEN = '\033[32m'
RED = '\033[31m'
EOC = '\033[0m'

ACCOUNT_ID = 'GC2BQYBXFOVPRDH35D5HT2AFVCDGXJM5YVTAF5THFSAISYOWAJQKRESK'
url = 'https://horizon.stellar.org/accounts/'+ACCOUNT_ID+'/payments?limit=200&order=asc'
lst = [[],[]]

stop = '2017-12-31T23:59:59Z'
again = True
p = 0

if (len(sys.argv) > 1):
    if (sys.argv[1] == "-p"):
        p = 1

while again:
    r = requests.get(url)
    for x in r.json()['_embedded']['records']:
        again = is_again(x, stop, again)# modif pour multi curl
        if again == False:
            break
        if x['type'] == 'payment':
            if x['asset_type'] != 'native':
                lst = match_currency(lst, x['asset_code'], x)
                print_transactions(x, p)
    url = r.json()['_links']['next']['href']

print_balance_accounts(lst)
# print a
