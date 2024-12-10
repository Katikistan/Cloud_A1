import toga
from toga.style import Pack
from toga.style.pack import COLUMN

def make_logout_box(self):
    self.logout_box.clear()
    logout_button = toga.Button(
        "Logout", 
        on_press=self.logout_handler, 
        style=Pack(padding=5)
    )
    self.logout_box.add(logout_button)
    self.login_box.refresh()       
