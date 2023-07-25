import pymysql.cursors

connection = pymysql.connect(
    host="sql6.freemysqlhosting.net",
    user="sql6635129",
    password="UD9PIExeur",
    db="sql6635129",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor,
)

if connection.open:
    print("the connection is opened")
