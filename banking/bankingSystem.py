'''
A simplified version of banking system

1. the banking system should support creating new accounts, 
    depositing money into accounts, and transferring money between two accounts

2. the banking system should support ranking accounts based on the total value 
    of outgoing transactions.

3. the banking system should allow scheduling payments and checking status of
    scheduled payments.

4. the banking system should support mering two account while retaining both
    accounts' balance and transaction histories.

'''

import account
import heapq
from collections import defaultdict

class BankingSystem:


    def __init__(self):
        self.account_dict = {}
        self.account_no = 0
        self.scheduled_payments = dict()
        self.scheduled_ordinal_no = 1
        self.scheduled_payments_queue = []
    

    def create_account(self, timestamp, account_id):
        '''
        create a new account with the given identifier if it does not already exists.
        return true if the account was successfully created or false if an account with
        accountid already exists.
        '''
        self.process_payments(timestamp)
        if account_id in self.account_dict:
            return False
        new_account = account.Account(account_id)
        self.account_dict[account_id] = new_account
        return True
    

    def deposit(self, timestamp, account_id, amount):
        '''
        should deposit the given amount of money to the specific accountid.
        return a string representing the total amount of money in the account after
        the query has been processed.
        if the specified account does not exist, should return an empty string.
        '''
        self.process_payments(timestamp)
        if account_id not in self.account_dict:
            return ""
        deposit_account = self.account_dict[account_id]
        deposit_account.deposit(amount)
        return str(deposit_account.get_balance())


    def transfer(self, timestamp, source_account_id, target_account_id, amount):
        '''
        should transfer the given amount of money from source account to target account. 
        return a string representing the balance of source account if the transfer is successful or 
        an empty string otherwise
            - cond1: return an empty string if source account or target account does not exist.
            - cond2: return an empty string if source account and target account are the same.
            - cond3: return an empty string if source account has insufficient funds to perform the transfer.
        '''
        self.process_payments(timestamp)
        # cond1
        if source_account_id not in self.account_dict or target_account_id not in self.account_dict:
            return ""
        
        # cond2
        if source_account_id == target_account_id:
            return  ""
        
        source_account = self.account_dict[source_account_id]
        target_account = self.account_dict[target_account_id]

        # cond3
        if source_account.get_balance() < amount:
            return ""
        
        source_account.transferOut(amount)
        target_account.deposit(amount)

        return str(source_account.get_balance())


    def top_spenders(self, timestamp, n):
        '''
        should return identifiers of the top n accounts with the highest amount of outgoing transactions.
        - the total amount of money either transfered out of or paid/withdrawn (via the schedule_payment operation
        which will be introduced in level 3)
        - sorting in descending order. in case of a tie, sorted alphabetically by account id in ascending order.
        the output should be a string in the following format: "accountid1 (total_outgoing1), accountid2 (
        total_outgoing2), ... 
        - if less than n accounts exist in the system, then return all their identifiers. 
        '''
        self.process_payments(timestamp)
        outgoing_order = []
        for account_id, account in self.account_dict.items():
            out_balance = account.get_outgoing()
            heapq.heappush(outgoing_order, (-out_balance, account_id, account))
        
        top_n = []
        while n > 0:
            out_balance, account_id, account = heapq.heappop(outgoing_order)
            top_n.append([-out_balance, account_id])
            n -= 1
        
        out_str = ""
        for i in top_n:
            out_str = out_str + str(i[1]) + "(" + str(i[0]) + ") ,"
        
        return out_str


    def schedule_payment(self, timestamp, account_id, amount, delay):
        '''
        the system should allow scheduling payments and checking the status of scheduled payments.
        should schedule a payment which will be performed at timestamp + delay.
        
        returns a string with a unique identifier for the scheduled payment in the
        following format: "payment[ordinal number of the scheduled payment across all accounts]
        if account_id does not exist, should return an empty string.
        the payment is skipped if the specified account has insufficient funds when
        the payment is performed.

        addition conditions:
            1. successful payments should be considered outgoing transactions and included when
            ranking accounts using top-spenders.
            2. scheduled payments should be processed before any other transactions at the given
            timestamp
            3. if an account needs to perform several scheduled payments simultaneously,
            they should be processed in order of creation.
        '''

        if account_id not in self.account_dict:
            return ""
        
        payment_time = timestamp + delay
        unique_identifier = f"payment{self.scheduled_ordinal_no}"

        scheduled_payment = ScheduledPayment(unique_identifier, account_id, self.scheduled_ordinal_no, payment_time, amount)
        
        self.scheduled_payments[self.scheduled_ordinal_no] = scheduled_payment
        heapq.heappush(self.scheduled_payments_queue, (scheduled_payment.payment_time, scheduled_payment.ordinal_no, scheduled_payment))

        self.scheduled_ordinal_no += 1
        return unique_identifier
    
    def process_payments(self, timestamp):

        while self.scheduled_payments_queue[0][0] <= timestamp:
            payment = heapq.heappop(self.scheduled_payments_queue)[2]
            if payment.ordinal_no not in self.scheduled_payments or payment.status == 0:
                continue
            account = payment.account_id
            account.transferOut(payment.amount)
            del self.scheduled_payments[payment.ordinal_no]
    
    def cancel_payment(self, timestamp, account_id, payment_id):
        '''
        should cancel the scheduled payment with payment_id. return true
        if the scheduled payment is successfully canceled. if payment_id
        does not exist or was already canceled, or if account_id is different
        from the source account for the scheduled payment, return false.
        note that scheduled payments must be performed before any cancel
        payment opertations at the given timestamp
        '''
        self.process_payments(timestamp)
        if account_id not in self.account_dict or payment_id not in self.scheduled_payments:
            return False
        
        payment = self.scheduled_payments[payment_id]
        if payment.account_id != account_id:
            return False
        
        payment.status = 0
        del self.scheduled_payments[payment_id]
        return True

        
class ScheduledPayment:

    def __init__(self, payment_id, account_id, schedule_ordinal_no, payment_time, amount):
        self.payment_id = payment_id
        self.account_id = account_id
        self.ordinal_no = schedule_ordinal_no
        self.payment_time = payment_time
        self.amount = amount
        self.status = 1
    

        
