import sys
import psycopg2
import UserPanel
import LoginWindow
import hashlib


# connection = psycopg2.connect(
#   database="kp0092_27",
#   user="st0092",
#   password="qwerty92",
#   host="172.20.8.18",
#   port="5432"
# )
# connect_cursor = connection.cursor()
#
# start_window = LoginWindow.LoginWindow(connect_cursor)
# access_level = start_window.create_window()
#
# if access_level == -1:
#   sys.exit(1)
#
# if access_level == 1:  # 0
#   user_window = UserPanel.UserPanel(connect_cursor)
#   user_window.create_window()
#
#
#
# connect_cursor.close()

user_window = UserPanel.UserPanel()
user_window.create_window()