from api.models import Event, Balance


def get_account_exist(account_id):
    """
    Function that receives an id of an account
    and returns false in case doesn't exist
    and the pk if exists
    """
    try:
        account_exist = Balance.objects.get(
            account_id=account_id)
        return account_exist
    except:
        return False


def create_account(account_id, amount):
    """
    Function that creates an account with id
    of destination and amount of transaction
    """
    create_account = Balance(
        account_id=account_id, balance=amount)
    create_account.save()


def update_balance(id, new_balance):
    """
    Function that updates the balance according with the amount field
    """
    Balance.objects.filter(pk=id).update(
        balance=new_balance)


def do_transaction(transaction, account_id1, amount, account_id2=''):
    """
    This function receives 3 mandatory parameters(transaction, account_id1,
    amount) and one optional(account_id2) in case of tranfer transactions.
    It's going to use the functions above, checking if account exists,
    updating balance, creating destination accounts.
    Only will return False if the origin account doesn't exists.
    Otherwise will follow the code returning to views.py and then
    execute the code in serializers.py
    """
    account_exist = get_account_exist(account_id1)
    if account_exist:
        if transaction == 'deposit':
            # if the account exists and the transaction is a deposit
            # the variable new_balance will receives the old balance
            # plus the amount of deposit
            new_balance = float(account_exist.balance) + \
                float(amount)
            update_balance(account_exist.account_id, new_balance)
        elif transaction == 'withdraw':
            # if the account exists and the transaction is a withdraw
            # the variable new_balance will receives the old balance
            # less the amount of withdraw
            new_balance = float(account_exist.balance) - \
                float(amount)
            update_balance(account_exist.account_id, new_balance)
        elif transaction == 'transfer':
            # if the origin account exists and the transaction is a transfer
            # the variable new_balance_origin will receives the old balance
            # of origin account subtract the amount
            new_balance_origin = float(
                account_exist.balance) - float(amount)
            update_balance(account_id1, new_balance_origin)
            # verify if the destination account exists
            account_dest_exist = get_account_exist(account_id2)
            if account_dest_exist:
                # if the account of destination exists, the amount will be added
                # with the old balance
                new_balance_destination = float(
                    account_dest_exist.balance) + float(amount)
                update_balance(account_id2, new_balance_destination)
            else:
                # if the destination account doesn't exist, will be created
                create_account(account_id2, amount)
    elif not account_exist and transaction == 'deposit':
        # if the account doesn't exist, but the transaction is a deposit
        # the account will be created using the function create_account
        create_account(account_id1, amount)
    elif not account_exist and (transaction == 'withdraw' or transaction == 'transfer'):
        # it's going to return false, because it's no possible to make a withdraw or transfer
        # if the origin account doesn't exist
        return False


def new_representation(transaction, account_id1, new_data, type_account, account_id2=''):
    """
    This function creates the correct representation of the data, that it's requested 
    in ipkiss tester, after a transaction is made.
    """
    # deletes the unnecessary data, that won't be displayed
    del new_data['type']
    del new_data['destination']
    del new_data['origin']
    del new_data['amount']
    if transaction in ['deposit', 'withdraw']:
        account_exist = get_account_exist(account_id1)
        if account_exist:
            new_balance = account_exist.balance
            # this dictionary will be displayed after doing a transaction
            # of deposit or withdraw
            new_data[type_account] = {"id": account_id1,
                                      "balance": new_balance}
    elif transaction == 'transfer':
        account_origin_exist = get_account_exist(account_id1)
        if account_origin_exist:
            account_dest_exist = get_account_exist(account_id2)
            new_balance_origin = account_origin_exist.balance
            new_balance_destination = account_dest_exist.balance

            data_origin = {}
            data_destination = {}
            data_origin['origin'] = account_origin_exist.account_id
            data_origin['balance'] = new_balance_origin
            data_destination['destination'] = account_dest_exist.account_id
            data_destination['balance'] = new_balance_destination
            # this both dictionaries will be displayed after doing a transaction
            # of transfer
            new_data['origin'] = {"id": data_origin["origin"],
                                  "balance": data_origin["balance"]}
            new_data['destination'] = {"id": data_destination["destination"],
                                       "balance": data_destination["balance"]}
