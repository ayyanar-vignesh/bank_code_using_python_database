import mysql.connector
import string
import random

# Establishing the connection to MySQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345",
  database="nov11_db"
)

try:

    mycursor = mydb.cursor()
    mycursor.execute("create table customer_data(cus_id varchar(255),cus_name varchar(255),cus_wallet int,cus_password varchar(255))")
    print("table created successfully")
except:
    print("already this table has been created")
    

# Function to add customer data
def add_customer_data():
    sql = "INSERT INTO customer_data (cus_id, cus_name, cus_wallet, cus_password) VALUES (%s, %s, %s, %s)"
    
    cus_id = ''.join(random.choices(string.ascii_letters, k=7))
    new_cus_id = "IOB_" + cus_id

    print("The generated random string : " + str(new_cus_id))
    cus_name = input("Enter your name: ")
    print("Deposit amount: 1000 rupees only")
    deposit_amount = int(input("Enter your deposit amount: "))
    
    if deposit_amount == 1000:
        cus_password = input("Enter your password: ")
        val = (new_cus_id, cus_name, deposit_amount, cus_password)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Data added successfully")
    else:
        print("Please deposit exactly 1000 rupees.")

# Function to verify customer credentials (ID and password)
def verify_customer(cus_id, cus_password):
    verify_sql = "SELECT cus_wallet FROM customer_data WHERE cus_id = %s AND cus_password = %s"
    mycursor.execute(verify_sql, (cus_id, cus_password))
    result = mycursor.fetchone()
    return result

# Function to deposit additional amount into an existing customer's account
def deposit_amount():
    cus_id = input("Enter your customer ID: ")
    cus_password = input("Enter your password: ")

    # Verify if customer exists and credentials are correct
    result = verify_customer(cus_id, cus_password)
    
    if result:
        current_balance = result[0]
        print(f"Current balance: {current_balance}")
        deposit_amount = int(input("Enter the amount you want to deposit: "))

        # Update the wallet balance
        new_balance = current_balance + deposit_amount
        update_sql = "UPDATE customer_data SET cus_wallet = %s WHERE cus_id = %s"
        mycursor.execute(update_sql, (new_balance, cus_id))
        mydb.commit()
        print(f"Deposit successful! New balance: {new_balance}")
    else:
        print("Invalid customer ID or password. Please try again.")

# Function to withdraw amount from an existing customer's account
def withdraw_amount():
    cus_id = input("Enter your customer ID: ")
    cus_password = input("Enter your password: ")

    # Verify if customer exists and credentials are correct
    result = verify_customer(cus_id, cus_password)
    
    if result:
        current_balance = result[0]
        print(f"Current balance: {current_balance}")
        withdraw_amount = int(input("Enter the amount you want to withdraw: "))

        # Check if the withdrawal amount is less than or equal to the current balance
        if withdraw_amount <= current_balance:
            new_balance = current_balance - withdraw_amount
            update_sql = "UPDATE customer_data SET cus_wallet = %s WHERE cus_id = %s"
            mycursor.execute(update_sql, (new_balance, cus_id))
            mydb.commit()
            print(f"Withdrawal successful! New balance: {new_balance}")
        else:
            print("Insufficient funds.")
    else:
        print("Invalid customer ID or password. Please try again.")

# New Function: Show Balance
def show_balance():
    cus_id = input("Enter your customer ID: ")
    cus_password = input("Enter your password: ")

    # Verify if customer exists and credentials are correct
    result = verify_customer(cus_id, cus_password)
    
    if result:
        current_balance = result[0]
        print(f"Your current balance is: {current_balance} rupees.")
    else:
        print("Invalid customer ID or password. Please try again.")



print("press 1->add a customer")
print("press 2->deposit")
print("press 3->withdraw")
print("press 4->show balance")

your_number=int(input("enter your number:"))
if your_number==1:
    add_customer_data()
elif your_number==2:
    deposit_amount()
elif your_number==3:
    withdraw_amount()
elif your_number==4:
    show_balance()
else:
    print("pls type 1 2 3 4 only")
