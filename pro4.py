import cx_Oracle
from account import *
from customer import customer
import datetime
from fileinput import close
now = datetime.datetime.now()
# global cust
# global acc
def printClosedAccountHistory():
    con = cx_Oracle.connect('system/sys1234@127.0.0.1/XE')
    cur = con.cursor()
    
    cur.execute("SELECT * FROM account where status='Deactive' ")
    results = cur.fetchall()
    if(int(cur.rowcount)>0):
        print('Closed account History')
        for row in results:
            acc_no = row[1]
            closedt = row[6]
            print(acc_no," ",closedt)
def signUp():
    print('in sign up')
    First_name = input("Enter First name")
    Last_name = input("Enter Last name")
    Address_line1 = input("Enter Your Address line 1")
    Address_line2 = input("Enter Your Address line 2")
    City = input("Enter your city")
    Pincode = input("Enter Pin code")
    Pincode = int(Pincode)
     # State = raw_input("Enter state")
    Account_type = input("Enter account type 'saving / current'")
    password = input("Enter password")
    cust = customer("0",First_name,Last_name,Address_line1,Address_line2,Pincode,City,password)
    cust_id = cust.signUp()
    if(Account_type=='saving'):
        acc = savingaccount(now.strftime("%Y-%m-%d"),'0',0,cust_id,0)
    else:
        acc = currentaccount(now.strftime("%Y-%m-%d"),'0',5000,cust_id)
    acc.openAccount()
def login():
    global cust
    global acc
    returnvalue  = True
    cust_id = input("Enter Customer ID")
    password = input("Enter Password")
    con = cx_Oracle.connect('system/sys1234@127.0.0.1/XE')
    cur = con.cursor()
    cur.execute("SELECT * FROM customer_details where customer_no=:custid and cust_pass=:cust_pass",(cust_id,password))
    results = cur.fetchall()
    if(int(cur.rowcount)>0):
        for row in results:
            f_name = row[1]
            l_name = row[2]
            addrline1 = row[3]
            addrline2 = row[4]
            pincode = row[5]
            city = row[6]
            
            cust = customer(cust_id,f_name,l_name,addrline1,addrline2,pincode,city,password)
        print("Successfully login ")
        print("welcome "+f_name+" "+l_name)
        cur.execute("SELECT * FROM account where customer_no=:custid",(cust_id))
        results = cur.fetchall()
        if(int(cur.rowcount)>0):
            for row in results:
                acc_no = row[0]
                acc_type = row[1]
                openedDate = row[2]
                balance = row[3]
                closedDate = row[5]
                status = row[6]
            if(status == 'Active'):
                if(acc_type=='saving'):
                    cur.execute("SELECT * FROM saving_account where acc_no=:accno",(acc_no))
                    results = cur.fetchall()
                    if(int(cur.rowcount)>0):
                        for row in results:
                            withdrawcount = row[1]
                        acc = savingaccount(openedDate,acc_no,balance,cust_id,withdrawcount)
                else:
                    acc = currentaccount(openedDate,acc_no,balance,cust_id)
            else:
                print('Your account is not active')
                returnvalue = False
    else:
        returnvalue = False
        print('wrong user name or password')
    con.commit()
    con.close()
    return returnvalue
Quit = 1
while Quit==1:        
    print ("===========================================")
    print("1.Sign UP")
    print("2.Login")
    print("3.Admin Login")
    print("4.Quit")
    print ("===========================================")
    ch = input ("Enter your choice")
    if ch == '1':
        signUp()
    elif ch == '2':
        if(login()):
            option2 = 1
            while option2 == 1:
                print ("===========================================")
                print("1.Address Change")
                print("2.Money Deposit")
                print("3.Money Withdraw")
                print("4.Print Statement")
                print("5.Transfer Money")
                print("6.Account Closure")
                print("7.Customer logout")
                print ("===========================================")
                choice = input ("Enter your choice")
                if choice == '1':
                    print("in address change")
                    cust.changeAddress()
                elif choice == '2':
                    amnt = int(input("Enter deposit amount"))
                    acc.deposit(amnt)
                elif choice == '3':
                    amnt = int(input("Enter withdraw amount"))
                    acc.withdraw(amnt)
                elif choice == '4':
                    acc.printStatement();
                elif choice == '5':
                    amnt = int(input("Enter Transfer amount"))
                    acc_no = input("Enter Transfer account no")
                    acc.transfer(amnt,acc_no)
                elif choice == '6':
                    acc.accountClosure();
                elif choice == '7':
                    print('Successfully logout')
                    option2 = 0    
    elif ch == '3':
        username = input("Enter User name")
        upass = input("Enter Password")
        if(username=='admin' & upass=='admin'):
            Option2 = 1
            while option2 == 1:
                print ("===========================================")
                print("1.Print Closed Account History")
                print("2.Admin logout")
                print ("===========================================")
                choice = input ("Enter your choice")
                if choice == '1':
                    printClosedAccountHistory()
                elif choice == '2':
                    print('Successfully logout')
                    option2 = 0  
        print("Thanks for using this system")               
    elif ch == '4':
        Quit = 0
        print("Thanks for using this system")
            




