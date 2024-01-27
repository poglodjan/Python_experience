from db_connection import cnx_mssql

class Tasks(object):
    def __init__(self):
        self.cursor = cnx_mssql.cursor()
        
    def create_tables(self);
        qwery_0 = """CREATE TABLE Users(
    UserId int NOT NULL PRIMARY KEY,
    Email varchar(30),
    BirthdayDate datetime,
    CityId int,
    Alias varchar(20),
    AmountOfWallets int,
    TotalBalance decimal(10,2),
    InitialAvgBalance decimal(10,2)
);

CREATE TABLE LoginHistory(
    UserId int NOT NULL PRIMARY KEY,
    LoginDate datetime,
    IpAdress varchar(30),
    CONSTRAINT fk_Users foreign key (UserId) REFERENCES Users(UserId),
);"""
        self.cursor.execute(qwery_1)
        print("Done, tables have been created")

    def task_a(self):
        print("Task a:")
        qwery_1 = "BEGIN TRANSACTION delete from LoginHistory where LoginDate like '2022%' delete from Users where UserId in (1,2,3,4,5,6,7,8) COMMIT TRANSACTION"
        self.cursor.execute(qwery_1)
        print("Done, records have been executed")
        show1 = "select * from Users"
        self.cursor.execute(show1)
        rows = self.cursor.fetchall()
        for rec in rows:
            print(rec)

    def task_b(self):
        print("Task b:")
        for i in range(0,3): 
            qwery_2 = "BEGIN TRANSACTION insert into Users (UserId,Email,BirthdayDate,CityId,Alias) values ("+str(i+1)+", 'a@a.pl', '1999-09-03',8,'KAP') COMMIT TRANSACTION"
            self.cursor.execute(qwery_2)
        qwery_calculating = """BEGIN TRANSACTION update Users SET TotalBalance = 3000 where UserId in (1,2,3) update Users SET AmountOfWallets = ROUND(RAND() * 10, 0)+1 where 
        UserId in (1,2,3) update Users SET InitialAvgBalance = TotalBalance / AmountOfWallets COMMIT TRANSACTION"""
        self.cursor.execute(qwery_calculating)
        print("Done, records have been updated")
        show2 = "select * from Users"
        self.cursor.execute(show2)
        rows = self.cursor.fetchall()
        for rec in rows:
            print(rec)
    
    def task_c(self):
        print("Task c:")
        qwery_3 = "BEGIN TRANSACTION update Users SET TotalBalance = TotalBalance+1000 where UserId in (select UserId from Users) insert into Users (UserId,BirthdayDate,AmountOfWallets,TotalBalance) values (4,'2004-09-04',5,2000) COMMIT TRANSACTION"
        self.cursor.execute(qwery_3)
        print("Done, records have been updated")
        show3 = "select * from Users"
        self.cursor.execute(show3)
        rows = self.cursor.fetchall()
        for rec in rows:
            print(rec)
    
    def task_d(self):
        print("Task d:")
        for i in range(4,9): 
            qwery_4 = "begin TRANSACTION insert into Users (UserId,Email,BirthdayDate,CityId,Alias,AmountOfWallets, TotalBalance) values ("+str(i+1)+", 'a@a.pl', '1999-09-03',8,'KAP',ROUND(RAND() * 10, 0)+1,1000*(ROUND(RAND() * 10, 0)+1)) commit TRANSACTION"
            self.cursor.execute(qwery_4)
        self.cursor.execute(qwery_4)
        show4 = "select * from Users"
        self.cursor.execute(show4)
        rows = self.cursor.fetchall()
        for rec in rows:
            print(rec)
        
