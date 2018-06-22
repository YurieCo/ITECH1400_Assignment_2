import os.path
import tkinter as tk
from tkinter import messagebox

from pylab import plot, show, xlabel, ylabel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from bankaccount import BankAccount

debug = os.path


win = tk.Tk()
win.geometry("440x640") # Set window size here to '440x640' pixels
win.title ='FedUni Banking' # Set window title here to 'FedUni Banking'

# The account number entry and associated variable
account_number_var = tk.StringVar()
account_number_entry = tk.Entry(win, textvariable=account_number_var)
account_number_entry.focus_set()

# The pin number entry and associated variable.
# Note: Modify this to 'show' PIN numbers as asterisks (i.e. **** not 1234)
pin_number_var = tk.StringVar()
account_pin_entry = tk.Entry(win, text='PIN Number', textvariable=pin_number_var)

# The balance label and associated variable
balance_var = tk.StringVar()
balance_var.set('Balance: $0.00')
balance_label = tk.Label(win, textvariable=balance_var)

brand_title_var = tk.StringVar()
brand_title_var.set("FedUni Banking")
brand_label = None

# The Entry widget to accept a numerical value to deposit or withdraw
amount_entry_var = tk.StringVar('')
amount_entry = tk.Entry(win, textvariable=amount_entry_var)

# The transaction text widget holds text of the accounts transactions

transaction_text_widget = tk.Text(win, height=10, width=48)
scrolbar = tk.Scrollbar(win)
# The bank account object we will work with
account = BankAccount()

# ---------- Button Handlers for Login Screen ----------

def clear_pin_entry(event):
    '''Function to clear the PIN number entry when the Clear / Cancel button is clicked.'''
    pin_number_var.set('')
    account_number_var.set('')
    # Clear the pin number entry here

def handle_pin_button(event):
    '''Function to add the number of the button clicked to the PIN number entry via its associated variable.'''    
    data = pin_number_var.get()
    if len(data) < 4:
        data += event
        pin_number_var.set(data)
    # Limit to 4 chars in length

    # Set the new pin number on the pin_number_var
    

def log_in(event):
    '''Function to log in to the banking system using a known account number and PIN.'''
    global account
    global pin_number_var
    global account_number_var

    read = event+'.txt'
    # Create the filename from the entered account number with '.txt' on the end
    # Try to open the account file for reading
    accept_loging = False
    try:
        with open(str(read), 'r') as account_file:        # Open the account file for reading

            account_number   = account_file.readline()[:-1]      # First line is account number

            account_pin      = account_file.readline()[:-1]       # Second line is PIN number, raise exceptionk if the PIN entered doesn't match account PIN read
         
            if account_pin != pin_number_var.get():
                raise ValueError("Pin doesnt match")
            else:
                accept_loging = True

            account_balance  = float(account_file.readline()[:-1])      # Read third and fourth lines (balance and interest rate)

            account_interest = float(account_file.readline()[:-1])
            transaction_list = []
            # Section to read account transactions from file - start an infinite 'do-while' loop here

            # Attempt to read a line from the account file, break if we've hit the end of the file. If we
            # read a line then it's the transaction type, so read the next line which will be the transaction amount.
            # and then create a tuple from both lines and add it to the account's transaction_list   
            while True:     
                _type = account_file.readline()  [:-1]        # Attempt to read a line
                if not _type:                         # If we failed, then exit
                    break
                _amount = float(account_file.readline()[:-1])

                transaction_list.append((_type.strip(), _amount))
           
            account.account_number = account_number
            account.account_pin = account_pin
            account.balance =  account_balance
            account.account_interest = account_interest
            account.transaction_list = transaction_list
        # Close the file now we're finished with it (context manager is doing this for us)
    except ValueError:
        messagebox.showerror("Error", "Incorrect PIN")
        account = BankAccount()
        account.account_interest = .30
        account = account_number_var
        clear_pin_entry("event")
        account_number_entry.focus_force()
    except Exception:
            # Catch exception if we couldn't open the file or PIN entered did not match account PIN
        messagebox.showerror("Error", "file doesnt exists")
        account = BankAccount()
        clear_pin_entry("event")
        account_number_entry.focus_force()

        # Show error messagebox and & reset BankAccount object to default...

        #  ...also clear PIN entry and change focus to account number entry
    if accept_loging:
        remove_all_widgets()
        create_account_screen()
    # Got here without raising an exception? Then we can log in - so remove the widgets and display the account screen
    

# ---------- Button Handlers for Account Screen ----------

def save_and_log_out():
    '''Function  to overwrite the account file with the current state of
       the account object (i.e. including any new transactions), remove
       all widgets and display the login screen.'''
    global account
    account.save_to_file()
    # Save the account with any new transactions
    
    # Reset the bank acount object
    account = BankAccount()
    # Reset the account number and pin to blank
    account_pin_entry.set('')
    account_number_var.set('')
    # Remove all widgets and display the login screen again
    remove_all_widgets()

def perform_deposit():
    '''Function to add a deposit for the amount in the amount entry to the
       account's transaction list.'''
    global account    
    global amount_entry_var
    global balance_label
    global balance_var
   
    # Try to increase the account balance and append the deposit to the account file
    try:
        # Get the cash amount to deposit. Note: We check legality inside account's deposit method
        amount_to_depo = amount_entry_var.get()

        # Deposit funds
        account.deposit_funds(amount_to_depo)

        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.
        transaction_text_widget.configure(state='normal')
        trans = account.get_transaction_string()
        for k in len(trans):
            transaction_text_widget.insert(k, ''.join(map(trans[k])))

        # Change the balance label to reflect the new balance
        balance_var.set('Balance: {}'.format(account.balance))
        # Clear the amount entry
        amount_entry.set('')
        # Update the interest graph with our new balance
        account.save_to_file()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        transaction_text_widget.configure(state='disabled')



    # Catch and display exception as a 'showerror' messagebox with a title of 'Transaction Error' and the text of the exception
        
def perform_withdrawal():
    '''Function to withdraw the amount in the amount entry from the account balance and add an entry to the transaction list.'''
    global account    
    global amount_entry_var
    global amount_entry
    global balance_label
    global balance_var

    # Try to increase the account balance and append the deposit to the account file
    try:
        textamount = amount_entry_var.get()
        account.withdraw_funds(textamount)
        textamount = account.balance
        amount_entry.configure(state='normal')
        amount_entry_var.set('')
        amount_entry.configure(state='disabled')
        balance_var.set('Balance: {}'.format(textamount))
        balance_label = tk.Label(win, textvariable=balance_var)
        account.save_to_file()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        amount_entry.configure(state='normal')



        # Get the cash amount to deposit. Note: We check legality inside account's withdraw_funds method
        
        # Withdraw funds        

        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.

        # Change the balance label to reflect the new balance

        # Clear the amount entry

        # Update the interest graph with our new balance

    # Catch and display any returned exception as a messagebox 'showerror'
        

# ---------- Utility functions ----------

def remove_all_widgets():
    '''Function to remove all the widgets from the window.'''
    global win
    for widget in win.winfo_children():
        widget.grid_remove()

def read_line_from_account_file():
    '''Function to read a line from the accounts file but not the last newline character.
       Note: The account_file must be open to read from for this function to succeed.'''
    global account_file
    return account_file.readline()[0:-1]


def plot_interest_graph():
    '''Function to plot the cumulative interest for the next 12 months here.'''

    # YOUR CODE to generate the x and y lists here which will be plotted
    P = account.balance
    x = []
    y = []
    for idx in range(1, 13):
        x.append(idx)
        val = P * (1 + account.account_interest / 12) ** (idx * 12)
        y.append(val)
        P = val

    # This code to add the plots to the window is a little bit fiddly so you are provided with it.
    # Just make sure you generate a list called 'x' and a list called 'y' and the graph will be plotted correctly.
    figure = Figure(figsize=(5, 2), dpi=100)
    figure.suptitle('Cumulative Interest 12 Months')
    a = figure.add_subplot(111)
    a.plot(x, y, marker='o')
    a.grid()

    canvas = FigureCanvasTkAgg(figure, master=win)
    canvas.draw()
    graph_widget = canvas.get_tk_widget()
    graph_widget.grid(row=4, column=0, columnspan=5, sticky='nsew')


# ---------- UI Screen Drawing Functions ----------


def create_login_screen():
    '''Function to create the login screen.'''
    global win
    global brand_title_var
    global pin_number_var
    global account_pin_entry
    global account_number_entry
    win.resizable(width=False, height=False)    # Account number entry here

    # ----- Row 0 -----
    # 'FedUni Banking' label here. Font size is 32.
    brand_label = tk.Label(win, textvariable=brand_title_var, font=("Courier", 32))

    # ----- Row 1 -----
    account_number = tk.Label(win, text="Account Number / PIN")   # Acount Number / Pin label here
    account_pin_entry.config(width=14, show="*")
    account_number_entry.config( width=14)

     # ----- Row 2 -----
    # Buttons 1, 2 and 3 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    button1 = tk.Button(win, text="1", command=lambda: handle_pin_button("1"), width=12)
    button2 = tk.Button(win, text="2", command=lambda:handle_pin_button("2"),width=12)
    button3 = tk.Button(win, text="3", command=lambda:handle_pin_button("3"),width=12)


    # ----- Row 3 -----
    # Buttons 4, 5 and 6 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    button4 = tk.Button(win, text="4", command=lambda:handle_pin_button("4"),width=12)
    button5 = tk.Button(win, text="5", command=lambda:handle_pin_button("5"),width=12)
    button6 = tk.Button(win, text="6", command=lambda:handle_pin_button("6"),width=12)

    # ----- Row 4 -----
    # Buttons 7, 8 and 9 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    button7 = tk.Button(win, text="7", command=lambda:handle_pin_button("7"),width=12)
    button8 = tk.Button(win, text="8", command=lambda:handle_pin_button("8"),width=12)
    button9 = tk.Button(win, text="9", command=lambda:handle_pin_button("9"),width=12)


    # ----- Row 5 -----
    # Cancel/Clear button here. 'bg' and 'activebackground' should be 'red'. But calls 'clear_pin_entry' function.
    button_cancel = tk.Button(win, text="Cancel / Clear", command=lambda:clear_pin_entry("cancel"))
    button_cancel.config(activebackground="red", bg="red",width=12)

    # Button 0 here
    button0 = tk.Button(win, text="0", command=handle_pin_button, width=12)

    # Login button here. 'bg' and 'activebackground' should be 'green'). Button calls 'log_in' function.
    button_login = tk.Button(win,text="Log In",  width=12)
    button_login["command"] = lambda: log_in( account_number_entry.get())
    button_login.config( bg="green", activebackground="green")

    # ----- Set column & row weights -----
    win.rowconfigure((0, 1), weight=1)  # make buttons stretch when

    # Set column and row weights. There are 5 columns and 6 rows (0..4 and 0..5 respectively)
    brand_label.grid(row=0, columnspan=3, rowspan=2)
    account_number.grid(row=3,sticky='nswe')
    account_number_entry.grid(row=3, column=1, sticky='nswe')
    account_pin_entry.grid(row=3, column=2, sticky='nswe')

    button1.grid(row=4,sticky='nswe')
    button2.grid(row=4, column=1, sticky='nswe')
    button3.grid(row=4, column=2, sticky='nswe')

    button4.grid(row=5,sticky='nswe')
    button5.grid(row=5, column=1, sticky='nswe')
    button6.grid(row=5, column=2, sticky='nswe')

    button7.grid(row=6,sticky='nswe')
    button8.grid(row=6, column=1, sticky='nswe')
    button9.grid(row=6, column=2, sticky='nswe')

    button_cancel.grid(row=7,sticky='nswe')
    button0.grid(row=7, column=1,sticky="nswe")
    button_login.grid(row=7, column=2,sticky="nswe")

    columns, rows = win.grid_size()
    for x in range(columns):
        win.grid_columnconfigure(x, weight=1)
    for y in range(rows):
        win.grid_rowconfigure(y, weight=1)



def create_account_screen():
    '''Function to create the account screen.'''
    global balance_label
    global transaction_text_widget
    global balance_var
    global amount_entry
    global amount_entry_var
    global win
    # ----- Row 0 -----

    # FedUni Banking label here. Font size should be 24.
    brand_label = tk.Label(win, textvariable=brand_title_var, font=("Courier", 24))
    brand_label.grid(row=0, columnspan=3, rowspan=1)
    # ----- Row 1 -----
   # Account number label here
    account_number = tk.Label(win, text="Account Number: {}".format(account.account_number),width=20)
    account_number.grid(row=1)
   # Balance label here
    balance_label.grid(row=1, column=1)
    balance_var.set("Balance: {}$".format(account.balance))
    # Log out button here
    logout = tk.Button(win, text="Log Out", width=13, command=lambda: save_and_log_out())
    logout.grid(row=1, column=2)
    # ----- Row 2 -----
    # Amount label here
    amount = tk.Label(win, text="Amount($)")
    amount.grid(row=2, sticky="n")

    # Amount entry here
    amount_entry.grid(row=2, column=1, sticky="nw")
    # Deposit button here
    frame = tk.Frame(win)
    deposit = tk.Button(frame, text="deposite", command=lambda:perform_deposit())
    deposit.grid(row=0)
    # Withdraw button here
    withdraw = tk.Button(frame, text="withdraw", command=lambda: perform_withdrawal())
    withdraw.grid(row=0, column=1)
    frame.grid(row=2, column=2, columnspan = 5,sticky="nsew")
    # NOTE: Bind Deposit and Withdraw buttons via the command attribute to the relevant deposit and withdraw
    #       functions in this file. If we "BIND" these buttons then the button being pressed keeps looking as
    #       if it is still pressed if an exception is raised during the deposit or withdraw operation, which is
    #       offputting.
    
    
    # ----- Row 3 -----

    # Declare scrollbar (text_scrollbar) here (BEFORE transaction text widget)
    scrolbar.config(command=transaction_text_widget.yview )
    transaction_text_widget.config(yscrollcommand=scrolbar.set, relief=tk.RAISED)

    transaction_text_widget.grid(row=3, columnspan=3,sticky="nsew")
    scrolbar.grid(row=3, column=2,sticky="E")
    # Add transaction Text widget and configure to be in 'disabled' mode so it cannot be edited.
    # Note: Set the yscrollcommand to be 'text_scrollbar.set' here so that it actually scrolls the Text widget
    # Note: When updating the transaction text widget it must be set back to 'normal mode' (i.e. state='normal') for it to be edited

    # Now add the scrollbar and set it to change with the yview of the text widget


    # ----- Row 4 - Graph -----

    # Call plot_interest_graph() here to display the graph
    plot_interest_graph()

    # ----- Set column & row weights -----

    # Set column and row weights here - there are 5 rows and 5 columns (numbered 0 through 4 not 1 through 5!)
    columns, rows = win.grid_size()
    for x in range(columns):
        win.grid_columnconfigure(x, weight=1)
    for y in range(rows):
        win.grid_rowconfigure(y, weight=1)


# ---------- Display Login Screen & Start Main loop ----------

create_login_screen()
# create_account_screen()
win.mainloop()
