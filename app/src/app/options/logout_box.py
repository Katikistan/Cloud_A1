import toga
from toga.style import Pack
from toga.style.pack import COLUMN

def make_logout_box(self):
    logout_box = toga.Box(style=Pack(direction=COLUMN,flex=1))
    logout_button = toga.Button(
        "Logout", 
        on_press=self.logout_handler, 
        style=Pack(padding=5)
    )
    logout_box.add(logout_button)
    return logout_box