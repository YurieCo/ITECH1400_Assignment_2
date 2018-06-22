class BankAccount():

    def __init__(self):
        '''Constructor to set account_number to '0', pin_number to an empty string,
           balance to 0.0, interest_rate to 0.0 and transaction_list to an empty list.'''
        self.account_number = 0
        self.pin_number = ''
        self.balance = 0.0
        self.interest_rate = 0.0
        self.transaction_list = []



    def deposit_funds(self, amount):
        '''Function to deposit an amount to the account balance. Raises an
           exception if it receives a value that cannot be cast to float.'''
        try:
            amount = float(amount)
            self.balance = self.balance + amount
            if amount < 0:
                raise ValueError("you cannot deposit negative value")
            self.transaction_list.append(('Deposit',amount))
        except ValueError:
            raise  ValueError("cannot be negative")
        

    def withdraw_funds(self, amount):
        '''Function to withdraw an amount from the account balance. Raises an
           exception if it receives a value that cannot be cast to float. Raises
           an exception if the amount to withdraw is greater than the available
           funds in the account.'''
        try:
            amount = float(amount)
        except:
            raise ValueError("amount cannot be cast to float")

        if amount < 0 or self.balance < amount:
            raise ValueError("Either amount cannot be negative or you are trying to withdraw more than you have")
        self.transaction_list.append(('Withdraw',amount))
        self.balance = self.balance - amount
        
    def get_transaction_string(self):
        '''Function to create and return a string of the transaction list. Each transaction
           consists of two lines - either the word "Deposit" or "Withdrawal" on
           the first line, and then the amount deposited or withdrawn on the next line.'''
        l = []
        for _ in self.transaction_list:
            txt = '\n'.join([_[0], str(_[1])])
            l.append(txt)
        return '\n'.join(l)


    def save_to_file(self):
        '''Function to overwrite the account text file with the current account
           details. Account number, pin number, balance and interest (in that
           precise order) are the first four lines - there are then two lines
           per transaction as outlined in the above 'get_transaction_string'
           function.'''
        
        with open(self.account_number,'w') as f:
            # f.write(str(self.account_number))
            # f.write(str(self.pin_number))
            # f.write(str(self.balance))
            # f.write(str(self.interest_rate))
            content  = '\n'.join(map(str,[self.account_number, self.pin_number, self.balance, self.interest_rate]))
            f.writelines(content)
            transhitory = self.get_transaction_string()
            f.writelines(transhitory)

    def __str__(self):
        return self.account_number
