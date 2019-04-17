import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="library_admin",
    passwd="readmoarbooksM8",
    database="librarymanager",
    auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

mycursor.execute("DROP DATABASE IF EXISTS librarymanager")
mycursor.execute("CREATE DATABASE librarymanager")
mycursor.execute("USE libraryManager;")

mycursor.execute("CREATE TABLE IF NOT EXISTS BOOK(Title varchar(100), DDCallNumber varchar(50), "
                 "LOCCallNumber varchar(50), "
                 "Author varchar(50), Publisher varchar(50), PublishDate date, PageCount int, "
                 "PRIMARY KEY (Title) );")

mycursor.execute("CREATE TABLE IF NOT EXISTS USERS(UserID INT AUTO_INCREMENT PRIMARY KEY, UserName varchar(50), "
                 "Gender varchar(6), "
                 "BirthDate date, LoanStatus varchar(20) );")

mycursor.execute("CREATE TABLE IF NOT EXISTS BOOKCOPY(CopyNumber INT, Title varchar(100), DueDate date, "
                 "CONSTRAINT BOOKCOPY_PK PRIMARY KEY (Title, CopyNumber),"
                 "CONSTRAINT BOOKTITLE_FK FOREIGN KEY (Title) REFERENCES BOOK(Title));")

mycursor.execute("CREATE TABLE IF NOT EXISTS LIBRARIANS(UserID int PRIMARY KEY, "
                 "CONSTRAINT LIBRARIANUSER_FK FOREIGN KEY (UserID) REFERENCES USERS(UserID) );")

mycursor.execute("CREATE TABLE IF NOT EXISTS HISTORIES(HistoryID int, LibrarianID int, UserID int, "
                 "BookTitle varchar(100), BookCopyID int, "
                 "CheckoutDate date, DueDate date, ReturnDate date,"
                 "PRIMARY KEY (HistoryID),"
                 "CONSTRAINT HISTORYLIBRARIAN_FK FOREIGN KEY (LibrarianID) REFERENCES LIBRARIANS(UserID),"
                 "CONSTRAINT HISTORYUSER_FK FOREIGN KEY (UserID) REFERENCES USERS(UserID),"
                 "CONSTRAINT HISTORYBOOKCOPY_FK FOREIGN KEY (BookTitle, BookCopyID) "
                 "REFERENCES BOOKCOPY(Title, CopyNumber) );")

mydb.commit()
