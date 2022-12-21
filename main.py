import sys
import psycopg2
import UserPanel
import LoginWindow
import AdminPanel


connection = psycopg2.connect(
  database="kp0092_27",
  user="st0092",
  password="qwerty92",
  host="172.20.8.18",
  port="5432"
)
connect_cursor = connection.cursor()

start_window = LoginWindow.LoginWindow(connect_cursor)
access_level = start_window.create_window()

if access_level == -1:
  sys.exit(1)

if access_level == 0:  # 0
  user_window = UserPanel.UserPanel(connect_cursor, access_level)
  user_window.create_window()
else:
  admin_window = AdminPanel.AdminPanel(connect_cursor, access_level)
  admin_window.create_window()

connect_cursor.close()