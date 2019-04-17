import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="library_admin",
    passwd="readmoarbooksM8",
    database="librarymanager",
    auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

# mycursor.execute("SHOW TABLES")

# sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
# val = ("John", "Highway 21")
# mycursor.execute(sql, val)
#
# mydb.commit()
#
# print(mycursor.rowcount, "record inserted.")


# #implement at some point
# if __name__ == "__main__":
#     1

# _________________________________________________________

def get_books_in_circulation():

    sort_by = 'Title'

    ans = input('would you like to sort the results? ')

    if ans[0] == 'y' or ans[0] == 'Y':

        ans = input('would you like to sort by due date or title? ')

        if ans[0] == 'd' or ans[0] == 'D':
            sort_type = 'DueDate'

    sql = "SELECT Title, CopyNumber, DueDate FROM BOOKCOPY ORDER BY %s"
    val = (sort_by, )
    mycursor.execute(sql, val)

    selected_data = mycursor.fetchall()
    for book in selected_data:
        print(book[0] + ' copy#' + str(book[1]) + (' due: ' + str(book[2]) if book[2] is not None else ' -currently available'))


def check_in_book(user_name, book_title, book_copy):
    return


def remove_from_circulation():
    book_title = input('what book should be removed? ')

    sql = "SELECT BOOKCOPY.CopyNumber FROM BOOKCOPY WHERE BOOKCOPY.Title = %s"
    val = (book_title, )
    mycursor.execute(sql, val)

    results = mycursor.fetchall()
    print(results)
    for x in results:
        print(x)

    while 1:
        book_copy = input('which copy should be removed? ')
        if book_copy == 'exit':
            return

        for i in results:
            if int(book_copy) in i:
                break  # break out of while loop
        else:
            print("invalid copy number, try again or use 'exit'")
            continue  # executes if the loop exits naturally
        break

    sql = "DELETE FROM BOOKCOPY WHERE Title = %s and CopyNumber = %s"
    val = (book_title, book_copy)

    mydb.commit()

    print(book_title + ' copy#' + book_copy + ' has been removed')



def get_books_on_loan():

    sort_type = 'Title'

    ans = input('would you like to sort the results? ')

    if ans[0] == 'y' or ans[0] == 'Y':

        ans = input('would you like to sort by due date, title, or user? ')

        if ans[0] == 'd' or ans[0] == 'D':
            sort_type = 'DueDate'
        elif ans[0] == 'u' or ans[0] == 'U':
            sort_type = 'UserName'

    sql = "SELECT BOOK.Title, USERS.UserName, HISTORIES.CheckoutDate, HISTORIES.DueDate" \
          "FROM BOOK JOIN BOOKCOPY ON BOOK.Title = BOOKCOPY.Title" \
          "JOIN HISTORIES ON HISTORIES.BookCopyID = BOOKCOPY.CopyNumber" \
          "WHERE HISTORIES.ReturnDate == null" \
          "ORDER BY %s"

    mycursor.execute(sql, sort_type)
    myresult = mycursor.fetchall()

    print("books currently on loan: ")

    for x in myresult:
        print(x)


def add_book_to_circulation():

    book_title = input('what book would you like to add? ')
    author_name = input('who\'s the author? ')
    page_count = input('how many pages is it? ')

    add_book_with_params(book_title, author_name, page_count)


def add_book_with_params(book_title, author_name, page_count):

    sql = "SELECT COUNT(Title) FROM BOOKCOPY WHERE Title = %s;"
    val = (book_title,)
    mycursor.execute(sql, val)

    book_num = int(mycursor.fetchone()[0])

    if book_num == 0:
        sql = "INSERT INTO BOOK (Title, Author, PageCount) VALUES (%s, %s, %s)"
        val = (book_title, author_name, page_count)
        mycursor.execute(sql, val)

    sql = "INSERT INTO BOOKCOPY (CopyNumber, Title) VALUES (%s, %s)"
    val = (book_num + 1, book_title)
    mycursor.execute(sql, val)

    mydb.commit()
    print(book_title + ' has been put into circulation.\nthere are now ' + str(book_num + 1) +
          ' copies in circulation\n')


def user_status_report():
    return


def search():
    return


def checkout_book(librarian, user, book):
    return


def get_user_status_report(sort_type):
    return


def add_user():
    name = input('what\'s the user\'s name? ')
    gender = input('gender? ')
    birth_date = input('birthdate? ')
    return add_user_param(name, gender, birth_date)


def add_user_param(name, gender, birthdate):

    sql = "INSERT INTO USERS(UserName, Gender, BirthDate, LoanStatus) VALUES (%s, %s, %s, 'good');"
    val = (name, gender, birthdate)
    mycursor.execute(sql, val)

    mydb.commit()
    print(name + " is now a user")

    mycursor.execute("SELECT UserID FROM USERS ORDER BY UserID DESC;")
    output = mycursor.fetchall()[0]  # returns the most recent UserID
    return output


def add_librarian():

    user_id = add_user()

    sql = "INSERT INTO LIBRARIANS(UserID) VALUES (%s);"
    val = (user_id,)
    mycursor.execute(sql, val)

    mydb.commit()
    print(" and a librarian")


def add_librarian_param(name, gender, birthdate):

    user_id = add_user_param(name, gender, birthdate)

    sql = "INSERT INTO LIBRARIANS(UserID) VALUES (%s);"
    val = (user_id, )
    mycursor.execute(sql, val)

    mydb.commit()


def main_function():

    input_str = ''

    while 1:

        print("What would you like to do?\nOptions:\n"
              "add book,  search,  check out book,  check in book,\n"
              "remove book,  books in circulation,  books on loan,\n"
              "user status report, exit\n")
        input_str = input()

        # hack to act like a do-while loop
        if input_str == 'exit':
            break

        # python doesn't support switch statements :(
        if input_str == 'add book':
            add_book_to_circulation()
        elif input_str == 'search':
            search()
        elif input_str == 'check out book':
            checkout_book()
        elif input_str == 'check in book':
            check_in_book()
        elif input_str == 'remove book':
            remove_from_circulation()
        elif input_str == 'books in circulation':
            get_books_in_circulation()
        elif input_str == 'books on loan':
            get_books_on_loan()
        elif input_str == 'user status report':
            get_user_status_report()
        else:
            print('invalid input')


if __name__ == '__main__':
    main_function()

"""
#get books on loan
SELECT BOOK.Title, USERS.UserName, HISTORIES.CheckoutDate, HISTORIES.DueDate
FROM BOOK JOIN BOOKCOPY ON BOOK.Title = BOOKCOPY.Title
JOIN HISTORIES ON HISTORIES.BookCopyID = BOOKCOPY.CopyNumber
WHERE HISTORIES.ReturnDate == null;


#checkin
UPDATE HISTORIES
SET ReturnDate = current_date()
WHERE UserID = UserID and BookTitle = BookTitle and BookID = BookID;


#remove book copy from circulation
DELETE FROM BOOKCOPY WHERE Title = Title and CopyNumber = CopyNumber;


#add book to circulation
if count(BOOKCOPY.Title = 0) then
INSERT INTO BOOKCOPY VALUES (1, Title, null)
else
	INSERT INTO BOOKCOPY VALUES (count(bookcopy.title) + 1, Title, null)
end else;

#search


#________________________________________ do the rest in python first

#checkout


#get books in circulation


#get user status report




"""