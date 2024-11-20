import httpx
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from app.options.login_box import make_login_box
from app.options.logout_box import make_logout_box
from app.options.main_box import make_main_box
from app.options.all_instances_box import make_all_instances_box
from app.options.instance_box import make_instance_box

class CloudApp(toga.App):

    def startup(self):
        main_box = make_main_box(self)
        login_box = make_login_box(self)
        all_instances_box = make_all_instances_box(self)
        instance_box = make_instance_box(self)
        logout_box = make_logout_box(self)

        
        option_container = toga.OptionContainer(
            content=[
                toga.OptionItem("Main box", main_box),
                toga.OptionItem("Login", login_box),
                toga.OptionItem("All instances", all_instances_box),
                toga.OptionItem("Instance run", instance_box),
                toga.OptionItem("Logout", logout_box),
                ],
            on_select = self.option_item_changed,
            style=Pack(direction=COLUMN))

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = option_container
        self.main_window.show()

    async def option_item_changed(self,widget):
        print('[i] You have selected another Option Item!')  

    async def say_hello(self, widget):
        async with httpx.AsyncClient() as client:
            response = await client.get("https://jsonplaceholder.typicode.com/posts/42")

        payload = response.json()

        self.main_window.info_dialog(
            greeting(self.name_input.value),
            payload["body"],
        )
    
    async def login_handler(self, widget):
        async with httpx.AsyncClient() as client:
            response = await client.get("https://jsonplaceholder.typicode.com/posts/42") 
        payload = response.json()
        self.main_window.info_dialog(
            greeting(self.username_input.value),
            payload["body"],
        )

    async def logout_handler(self, widget):
        print("You want to logout!")

    async def role_changed(self, widget):
            self.selected_role_item = self.role_selection.value
            print(f"[i] You changed the role to {self.selected_role_item}!")
            
    async def execute_event(self, widget):
        print(f"[i] You want to execute event: {widget.id}")

    async def show_instance(self, widget):
            print(f"[i] You want to show {widget.id}")

    async def delete_instance_by_id(self, widget):
        print(f"[i] You want to delete {widget.id[1:]}")
        #self.instances = [inst for inst in self.instances if inst['id'] != _id]
            
    async def create_instance(self,widget):
        print(f"[i] Create new instance!")

    async def delete_all_by_id(self, widget):
        print(f"[i] Delete all instances!")

def greeting(name):
    if name:
        return f"Hello, {name}"   
     
def main():
    return CloudApp()
