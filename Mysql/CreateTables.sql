# 0.删除旧表
Set Foreign_Key_Checks = 0; 
Drop table if exists Sub_bank; 
Drop table if exists Employee; 
Drop table if exists Customer; 
Drop table if exists Check_account; 
Drop table if exists Deposit_account; 
Drop table if exists Loan; 
Drop table if exists Pay; 
Drop table if exists Customer_Deposit_account; 
Drop table if exists Customer_Check_account; 
Drop table if exists Loan_Customer; 
Drop table if exists Employee_Customer; 
Set Foreign_Key_Checks = 0; 

# 1.建立支行表
Create Table Sub_bank(
	Bank_name	Char(50), 
    City		Char(50), 
    Possession	Float	Default 0.0, 
    Bank_pass	Char(6)	Default '123456', 
    Constraint PK_Bank Primary Key (Bank_name)
);
# 2.建立员工表
Create Table Employee(
	Employee_id			BIGInt(16), 
    Employee_depart_id	Char(10), 
    Employee_bank_name	Char(32), 
    Employee_name		Char(50), 
    Employee_phone		Int(12), 
    Employee_address	Char(128), 
    Employee_enterdate		Date, 
    Employee_lead		Char(10), 
    Employee_password	Char(6)	Default '123456',
    Constraint PK_Employee Primary Key (Employee_id), 
    Constraint UQ_Leader Unique (Employee_lead)
);
# 3.建立客户表
Create Table Customer(
	Customer_id			BigInt(16), 
    Customer_name		Char(32), 
    Customer_phone		Int(12), 
    Customer_address	Char(128), 
    Customer_contact_name	Char(32), 
    Customer_contact_phone	Int(12), 
	Customer_contact_email	Char(64), 
    Customer_contact_relation	Char(32), 
    Customer_pass	Char(6),
    Constraint PK_Customer Primary Key (Customer_id)
);
# 4.建立支票账户表
Create Table Check_account(
	Check_account_id		Int(16), 
    Check_account_money		Float, 
    Check_account_regdate	Date, 
    Check_account_overdraft	Float, 
    Check_account_password	Char(6)	Default '123456', 
    Constraint PK_Check_account	Primary Key	(Check_account_id)
);
# 5.建立存储账户表
Create Table Deposit_account(
	Deposit_account_id		Int(16), 
    Deposit_account_money	Float, 
	Deposit_account_regdate	Date, 
    Deposit_account_interestrate		Float	Default 0.0, 
    Deposit_account_currencytype	Int(1), 
    Deposit_account_password		Char(6)	Default '123456',
    Constraint PK_Deposit_account Primary Key(Deposit_account_id)
);
# 6.建立贷款表
Create Table Loan(
	Loan_id		Int(16), 
    Bank_name	Char(50), 
    Loan_money	Float, 
    Status		Int(1), 
    Constraint PK_Loan Primary Key(Loan_id),
    Constraint FK_Bank_name Foreign Key(Bank_name) References Sub_Bank(Bank_name)
);
# 7.建立支付表
Create Table Pay(
	Loan_id		Int(16), 
    Pay_date	Date, 
    Pay_money	Float, 
    Constraint FK_Loan_id Foreign Key(Loan_id) References Loan(Loan_id)
);
# 8.建立客户-存储账户表
Create Table Customer_Deposit_account(
	Bank_name	Char(50), 
    Customer_id	Bigint(16), 
    Deposit_account_id	Int(16), 
    Last_view	Date, 
    Constraint PK_Customer_Deposit_account Primary Key(Bank_name, Customer_id), 
    Constraint FK_CD_Bank_name Foreign Key(Bank_name) References Sub_bank(Bank_name), 
    Constraint FK_CD_Customer_id Foreign Key(Customer_id) References Customer(Customer_id), 
    Constraint FK_CD_Deposit_account_id Foreign Key(Deposit_account_id) References Deposit_account(Deposit_account_id)
);
# 9.建立客户-支票账户表
Create Table Customer_Check_account(
	Bank_name	Char(50), 
    Customer_id	BigInt(16), 
    Check_account_id	Int(16), 
    Last_view	Date, 
    Constraint PK_Customer_Check_account Primary Key(Bank_name, Customer_id), 
    Constraint FK_CC_Bank_name Foreign Key(Bank_name) References Sub_bank(Bank_name), 
    Constraint FK_CC_Customer_id Foreign Key(Customer_id) References Customer(Customer_id), 
    Constraint FK_CC_Check_account_id Foreign Key(Check_account_id) References Check_account(Check_account_id)
);
# 10.建立客户贷款表
Create Table Loan_Customer(
	Loan_id	Int(16), 
    Customer_id	BigInt(16), 
    Constraint PK_Load_customer Primary Key(Loan_id, Customer_id), 
    Constraint FK_LC_Customer_id Foreign Key(Customer_id) References Customer(Customer_id), 
    Constraint FK_LC_Loan_id Foreign Key(Loan_id) References Loan(Loan_id)
);
# 11.建立员工客户表
Create Table Employee_Customer(
	Employee_id	BigInt(16),
	Customer_id	BigInt(16), 
    Servicetype	Char(16), 
    Constraint PK_Employee_Customer Primary Key(Employee_id, Customer_id), 
    Constraint FK_EC_Customer_id Foreign Key(Customer_id) References Customer(Customer_id), 
    Constraint FK_EC_Emplyee_id Foreign Key(Employee_id) References Employee(Employee_id)
);







