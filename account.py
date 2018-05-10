import cx_Oracle
import datetime
now = datetime.datetime.now()
class account:
    def __init__(self, openedDate, acc_no, balance, cust_id, ac_type):
        self.openedDate = openedDate
        self.acc_no = acc_no
        self.balance = balance
        self.cust_id = cust_id
        self.ac_type = ac_type
    def withdraw(self, amnt):
        if(self.balance>=amnt):
            self.balance = self.balance - amnt
            con = cx_Oracle.connect('system/sys1234@127.0.0.1/XE')
            cur = con.cursor()
            tr_id = 0
            cur.execute("SELECT tran_no FROM transaction")
            results = cur.fetchall()
            print(results)
            if(int(cur.rowcount)>0):
                for row in results:
                    tr_id = row[0]
                tr_id = int(tr_id) + 1
                self.balance = self.balance + amnt
            cur.execute(""" insert into transaction(:trans_id,:tr_date,:tr_type,:amount,:frm_acc,:to_acc)""",(tr_id,now.strftime("%Y-%m-%d"),'Withdraw',amnt,self.acc_no,self.acc_no))
            cur.execute("update account set balance=:bal where acc_no = :acc_no",(self.balance,self.acc_no))
            if(int(cur.rowcount)>0):
                print("Deposit successful")
            else:
                print("Problem in deposit operation")
            con.commit()
            con.close()
            print("Successfully withdraw")
            print("Your available balance is",self.balance)
    def deposit(self, amnt):
        con = cx_Oracle.connect('system/sys1234@127.0.0.1/XE')
        cur = con.cursor()
        tr_id = 0
        cur.execute("SELECT tran_no FROM transaction")
        results = cur.fetchall()
        print(results)
        if(int(cur.rowcount)>0):
            for row in results:
                tr_id = row[0]
        tr_id = int(tr_id) + 1
        self.balance = self.balance + amnt
        cur.execute(""" insert into transaction(:trans_id,:tr_date,:tr_type,:amount,:frm_acc,:to_acc)""",(tr_id,now.strftime("%Y-%m-%d"),'Deposit',amnt,self.acc_no,self.acc_no))
        cur.execute("update account set balance=:bal where acc_no = :acc_no",(self.balance,self.acc_no))
        
        if(int(cur.rowcount)>0):
            cur.execute("insert ",(self.balance,self.acc_no))
            print("Deposit successful")
        else:
            print("Problem in deposit operation")
        con.commit()
        con.close()
        print("Successfully deposit")
        print("Your available balance is",self.balance)
    def display(self):
        print( "account no :",self.acc_no)
        print( "customer Id:",self.cust_id)
        print( "Balance :",self.balance)
        print( "Opened Date:",self.openedDate)
        print("Account type: "+self.ac_type)
    def openAccount(self):
        tr_id = 0
        cur.execute("SELECT tran_no FROM transaction")
        results = cur.fetchall()
        print(results)
        if(int(cur.rowcount)>0):
            for row in results:
                tr_id = row[0]
        tr_id = int(tr_id) + 1
        acc_id = 0
        con = cx_Oracle.connect('system/sys1234@127.0.0.1/XE')
        cur = con.cursor()
        cur.execute("SELECT acc_no FROM account")
        results = cur.fetchall()
        print(results)
        if(int(cur.rowcount)>0):
            for row in results:
                acc_id = row[0]
        if(int(acc_id)==0):
            self.acc_no = 1
            cur.execute(""" insert into account values(:acc_no, :acc_type,:openedDate, :balance, :cust_no, :closingDate, :status)""",(self.acc_no,self.ac_type,self.openedDate,self.balance,self.cust_id,'','Active'))
            cur.execute(""" insert into transaction(:trans_id,:tr_date,:tr_type,:amount,:frm_acc,:to_acc)""",(tr_id,now.strftime("%Y-%m-%d"),'Opening Account',self.balance,self.acc_no,self.acc_no))
        else:
            self.acc_no = int(acc_id) + 1
            cur.execute(""" insert into account values(:acc_no, :acc_type, :openedDate, :balance, :cust_no, :closingDate, :status)""",(self.acc_no,self.ac_type,self.openedDate,self.balance,self.cust_id,'','Active'))
            cur.execute(""" insert into transaction(:trans_id,:tr_date,:tr_type,:amount,:frm_acc,:to_acc)""",(tr_id,now.strftime("%Y-%m-%d"),'Opening Account',self.balance,self.acc_no,self.acc_no))
        con.commit()
        con.close()
        print('Account opened with Id ',self.acc_no)
        self.display()
        return self.acc_no
    def accountClosure(self):
        con = cx_Oracle.connect('system/sys1234@127.0.0.1/XE')
        cur = con.cursor()
        cur.execute("update account set status='Deactive' , closedDate= :closeDate where acc_no = :acc_no",(now.strftime("%Y-%m-%d"),self.acc_no))
        if(int(cur.rowcount)>0):
            print("Account closure successful")
        else:
            print("Problem in account closure")
        con.commit()
        con.close()
    def printStatement(self):
        frm_Date = input("Enter from date:(2017-10-20)")
        to_Date = input("Enter to date:(2017-10-20)")
        con = cx_Oracle.connect('system/sys123@127.0.0.1/XE')
        cur = con.cursor()
        cur.execute("select * from transaction where acc_no=:acc_no and tr_date between :frmDt and :toDt",(self.acc_no,frm_Date,to_Date))
        records = cur.fetchall()
        if(int(cur.rowcount)>0):
            for row in records:
                print(row[0]," ",row[1]," ",row[2]," ",row[3]," ",row[4]," ",row[5]," ",row[6]," ",row[7])
        else:
            print("Problem in print statement")
        con.commit()
        con.close()
    def transfer(self,amnt,acc_no):
        self.balance = self.balance - amnt
        con = cx_Oracle.connect('system/sys1234@127.0.0.1/XE')
        cur = con.cursor()
        tr_id = 0
        cur.execute("SELECT tran_no FROM transaction")
        results = cur.fetchall()
        print(results)
        if(int(cur.rowcount)>0):
            for row in results:
                tr_id = row[0]
        tr_id = int(tr_id) + 1
        cur.execute("insert into transaction values(:trans_id,:tr_date,:tr_type,:amount,:frm_acc,:to_acc)",(tr_id,now.strftime("%Y-%m-%d"),'Transfer',amnt,self.acc_no,acc_no))
        cur.execute("update account set balance=:bal where acc_no = :acc_no",(self.balance,self.acc_no))#deduct account
        cur.execute("update account set balance= balance + :bal where acc_no = :acc_no",(amnt,acc_no))
        if(int(cur.rowcount)>0):
            cur.execute("insert ",(self.balance,self.acc_no))
            print("Deposit successful")
        else:
            print("Problem in deposit operation")
        con.commit()
        con.close()
class savingaccount(account):
    withdraw_limit = 2
    def __init__(self, openedDate, acc_no, balance, cust_id,withd):
        account.__init__(self, openedDate, acc_no, balance, cust_id,'saving')
        self.totalwithdraw = withd
        
    def withdraw(self, amnt):
        if(self.totalwithdraw<=self.withdraw_limit):
            self.totalwithdraw += 1
            account.withdraw(self, amnt)
            con = cx_Oracle.connect('system/sys1234@127.0.0.1/XE')
            cur = con.cursor()
            cur.execute("update saving_account set withdrawCount=:wtc where acc_no = :acc_no",(self.totalwithdraw,self.acc_no))
#             if(int(cur.rowcount)>0):
#                 print("Deposit successful")
#             else:
#                 print("Problem in deposit operation")
#             con.commit()
#             con.close()
            print("Successfully withdraw")
            print("Your available balance is",self.balance)
        else:
            print('total withdraw is more than limit!!!')
    def openAccount(self):
        acc_no = account.openAccount(self)
        con = cx_Oracle.connect('system/sys1234@127.0.0.1/XE')
        cur = con.cursor()
        cur.execute(""" insert into saving_account values(:acc_no, :withdrawcount)""",(acc_no,self.totalwithdraw))
        con.commit()
        con.close()
        return acc_no
class currentaccount(account):
    minimum_balance = 5000
    def __init__(self, openedDate, acc_no, balance, cust_id):
        account.__init__(self, openedDate, acc_no, balance, cust_id, 'current')
    def withdraw(self, amnt):
        if(self.balance-amnt>self.minimum_balance):
            account.withdraw(self, amnt)
        else:
            print('please maintain minimum balance')
    def openAccount(self):
        acc_no = account.openAccount(self)
        con = cx_Oracle.connect('system/sys1234@127.0.0.1/XE')
        cur = con.cursor()
        cur.execute(""" insert into current_account values(:acc_no)""",(acc_no))
        con.commit()
        con.close()
        return acc_no
