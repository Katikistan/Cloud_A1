import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import httpx

def make_login_box(self):
    self.login_box.clear()
    #login_box = toga.Box(style=Pack(direction=COLUMN))
    
    username_label = toga.Label("Username: ", style=Pack(padding=(0, 5)))
    self.username_input = toga.TextInput(style=Pack(flex=1))
    username_box = toga.Box(style=Pack(direction=ROW, padding=5))
    username_box.add(username_label)
    username_box.add(self.username_input)

    password_label = toga.Label("Password: ", style=Pack(padding=(0, 5)))
    self.password_input = toga.PasswordInput(style=Pack(flex=1))
    password_box = toga.Box(style=Pack(direction=ROW, padding=5))
    password_box.add(password_label)
    password_box.add(self.password_input)

    login_button = toga.Button("Login", on_press=self.login_handler, style=Pack(padding=5))

    self.login_box.add(username_box)
    self.login_box.add(password_box)
    self.login_box.add(login_button)

    #return login_box
    self.login_box.refresh()       

