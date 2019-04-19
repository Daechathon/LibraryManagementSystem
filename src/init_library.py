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

# BOOK
mycursor.execute("CREATE TABLE IF NOT EXISTS BOOK(Title varchar(100), DDCallNumber varchar(50), "
                 "LOCCallNumber varchar(50), "
                 "Author varchar(50), Publisher varchar(50), PublishDate date, PageCount int, "
                 "PRIMARY KEY (Title) );")
print('book table created')

# USERS
mycursor.execute("CREATE TABLE IF NOT EXISTS USERS(UserID INT AUTO_INCREMENT PRIMARY KEY, UserName varchar(50), "
                 "UserLastName varchar(50), Gender varchar(6), "
                 "BirthDate date, LoanStatus varchar(20) );")
print('users table created')

# BOOKCOPY
mycursor.execute("CREATE TABLE IF NOT EXISTS BOOKCOPY(CopyNumber INT, Title varchar(100), DueDate date, "
                 "CONSTRAINT BOOKCOPY_PK PRIMARY KEY (Title, CopyNumber),"
                 "CONSTRAINT BOOKTITLE_FK FOREIGN KEY (Title) REFERENCES BOOK(Title));")
print('bookcopy table created')

# LIBRARIANS
mycursor.execute("CREATE TABLE IF NOT EXISTS LIBRARIANS(UserID int PRIMARY KEY, "
                 "CONSTRAINT LIBRARIANUSER_FK FOREIGN KEY (UserID) REFERENCES USERS(UserID) );")
print('librarians table created')

# HISTORIES
mycursor.execute("CREATE TABLE IF NOT EXISTS HISTORIES(HistoryID int PRIMARY KEY AUTO_INCREMENT, " 
                 "LibrarianID int, UserID int, "
                 "BookTitle varchar(100), BookCopyID int, "
                 "CheckoutDate date, DueDate date, ReturnDate date,"
                 "CONSTRAINT HISTORYLIBRARIAN_FK FOREIGN KEY (LibrarianID) REFERENCES LIBRARIANS(UserID),"
                 "CONSTRAINT HISTORYUSER_FK FOREIGN KEY (UserID) REFERENCES USERS(UserID),"
                 "CONSTRAINT HISTORYBOOKCOPY_FK FOREIGN KEY (BookTitle, BookCopyID) "
                 "REFERENCES BOOKCOPY(Title, CopyNumber) );")
print('histories table created')


mydb.commit()
