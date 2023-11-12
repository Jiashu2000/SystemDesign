'''
A simplified version of banking system

1. the banking system should support creating new accounts, 
    depositing amount into accounts, and transferring amount between two accounts

2. the banking system should support ranking accounts based on the total value 
    of outgoing transactions.

3. the banking system should allow scheduling payments and checking status of
    scheduled payments.

4. the banking system should support mering two account while retaining both
    accounts' balance and transaction histories.

'''


class Account:


    def __init__(self, account_id) -> None:
        self.account_id = account_id
        self.balance = 0
        self.outgoing = 0
    
    def deposit(self, amount):
        self.balance += amount
    
    def get_balance(self):
        return self.balance

    def get_outgoing(self):
        return self.outgoing
    
    def transferOut(self, amount):
        if self.has_sufficient_balance(amount):
            self.balance -= amount
            self.outgoing += amount
            return True
        return False

    def has_sufficient_balance(self, amount):
        if self.balance < amount:
            return False
        return True

        