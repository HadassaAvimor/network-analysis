import os

import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()

connection = pymysql.connect(
    host="sql6.freemysqlhosting.net",
    user=os.environ["DB_USERNAME"],
    password=os.environ["DB_PASSWORD"],
    db=os.environ["DB"],
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor,
)



