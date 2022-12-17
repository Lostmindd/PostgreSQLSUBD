import psycopg2
import LoginWindow
import hashlib


connection = psycopg2.connect(
  database="kp0092_27",
  user="st0092",
  password="qwerty92",
  host="172.20.8.18",
  port="5432"
)

connect_cursor = connection.cursor()



start_window = LoginWindow.LoginWindow(connect_cursor)
start_window.create_window()


connect_cursor.close()