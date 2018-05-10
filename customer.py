import cx_Oracle
class customer:
    def __init__(self, cus_id, c_fname,c_lname,line1,line2,pincode,city,password):
        self.cus_id = cus_id
        self.c_fname = c_fname
        self.c_lname = c_lname
        self.password = password
        self.line1 = line1
        self.line2 = line2
        self.pincode = pincode
        self.city = city
    def verifyPassword(self,cpass):
        if(self.password==cpass):
            return True
        else:
            return False
    def signUp(self):
        con = cx_Oracle.connect('system/sys1234@127.0.0.1/XE')
        cur = con.cursor()
        cust_id = 0
        cur.execute("SELECT customer_no FROM customer_details")
        results = cur.fetchall()
        print(results)
        print(cur.rowcount)
        if(int(cur.rowcount)>0):
            for row in results:
                cust_id = row[0]
        if(int(cust_id)==0):
            self.cus_id = 1
            cur.execute(""" insert into customer_details values(:cust_id, :cust_fname, :cust_lname, :cust_addr1, :cust_addr2, :cust_pin, :cust_city,
             :cust_pass)""",(self.cus_id,self.c_fname,self.c_lname,self.line1,self.line2,self.pincode,self.city,self.password))
        else:
            self.cus_id = int(cust_id) + 1
            cur.execute(""" insert into customer_details values(:cust_id, :cust_fname, :cust_lname, :cust_addr1, :cust_addr2, :cust_pin, :cust_city,
             :cust_pass)""",(self.cus_id,self.c_fname,self.c_lname,self.line1,self.line2,self.pincode,self.city,self.password))
        con.commit()
        con.close()
        print("customer id : ",self.cus_id)
        return  self.cus_id
    def changeAddress(self):
        print('inside address change',self.cus_id)
        Address_line1 = input("Enter Your Address line 1")
        Address_line2 = input("Enter Your Address line 2")
        City = input("Enter your city")
        Pincode = input("Enter Pin code")
        Pincode = int(Pincode)
        con = cx_Oracle.connect('system/sys1234@127.0.0.1/XE')
        cur = con.cursor()
        cur.execute(""" update customer_details set addr_line1=:cust_addr1,addr_line2=:cust_addr2, pincode=:cust_pin, city=:cust_city where customer_no=:cust_id)""",(Address_line1,Address_line2,Pincode,City,self.cus_id))
        if(int(cur.rowcount)>0):
            print("Successfully Updated")
        else:
            print("Problem in address update")
        con.commit()
        con.close()