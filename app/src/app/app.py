import httpx
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from app.options.login_box import make_login_box
from app.options.logout_box import make_logout_box
from app.options.all_instances_box import make_all_instances_box
from app.options.instance_box import make_instance_box
from app.services.dcr_active_repository import check_login_from_dcr, DcrActiveRepository, DcrUser

class CloudApp(toga.App):
    graph_id = 1986525
    dcr_ar = None 

    def startup(self):
        self.login_box = toga.Box(style=Pack(direction=COLUMN))
        self.instances = {}        
        self.all_instances_box = toga.Box(style=Pack(direction=COLUMN,flex=1))
        self.instance_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        self.logout_box = toga.Box(style=Pack(direction=COLUMN, flex=1))

        make_login_box(self)
        
        self.option_container = toga.OptionContainer(
            content=[
                toga.OptionItem("Login", self.login_box),
                toga.OptionItem("All instances", self.all_instances_box),
                toga.OptionItem("Instance run", self.instance_box),
                toga.OptionItem("Logout", self.logout_box),
                ],
            on_select = self.option_item_changed,
            style=Pack(direction=COLUMN))
        # disable all options except login
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.option_container
        self.main_window.show()

        self.option_container.content['All instances'].enabled = False  
        self.option_container.content['Instance run'].enabled = False
        self.option_container.content['Logout'].enabled = False


    async def option_item_changed(self,widget):
        print('[i] You have selected another Option Item!')
        if widget.current_tab.text == 'All instances':
            await self.show_instances_box()


    async def login_handler(self, widget):
        connected = await check_login_from_dcr(self.username_input.value,self.password_input.value)

        if connected:
            self.dcr_user = DcrUser(self.username_input.value,self.password_input.value)
            self.dcr_ar = DcrActiveRepository(self.dcr_user)
            make_logout_box(self)

            self.option_container.content['All instances'].enabled = True
            self.option_container.content['Instance run'].enabled = True
            self.option_container.content['Logout'].enabled = True
            self.option_container.current_tab = 'All instances'
            self.option_container.content['Login'].enabled = False 
                
            print(f"[i] You are logged in as {self.username_input.value}!")
        else:
            print(f"[x] Login failed!")
            
        # await make_login_box(self)

    async def logout_handler(self, widget):
        print("You want to logout!")
        self.username_input.value = None
        self.password_input.value = None
        self.option_container.content['Login'].enabled = True
        self.option_container.current_tab = 'Login'
        self.option_container.content['Logout'].enabled = False
        self.option_container.content['All instances'].enabled = False
        self.option_container.content['Instance run'].enabled = False
        

    async def role_changed(self, widget):
            self.selected_role_item = self.role_selection.value
            print(f"[i] You changed the role to {self.selected_role_item}!")
            
    async def execute_event(self, widget):
        print(f"[i] You want to execute event: {widget.id}")

    async def show_instance(self, widget):
        print(f"[i] You want to show {widget.id}")
        self.current_instance_id = widget.id
        self.option_container.current_tab = "Instance run"
        await self.show_instance_box()
    
    async def show_all_instance(self, widget):
        print(f"[i] You want to show {widget.id}")
        self.current_instance_id = widget.id
        self.option_container.current_tab = "All instances"
        await self.all_instances_box()

    #del 1, C3
    async def show_instances_box(self):
        await make_all_instances_box(self)

    #cel 1, C5
    async def show_instance_box(self):
        await make_instance_box(self)
    
    async def delete_instance_by_id(self, widget):
        print(f"[i] You want to delete {widget.id[1:]}")
        instance_id = widget.id[1:]
        status_code = await self.dcr_ar.delete_instance(self.graph_id,instance_id)
        if status_code == 200:
            print(f"[i] Successfully deleted instance with id: {instance_id}")
        else:
            print(f"[x] Failed to delete instance with id: {instance_id} status code: {status_code}")
        await self.show_instances_box()
            
    async def create_instance(self,widget):
        self.current_instance_id = await self.dcr_ar.create_new_instance(self.graph_id)
        self.option_container.current_tab = "Instance run"
        await self.show_instance_box()
        
    async def delete_all_by_id(self, widget):
        print(f"[i] You want to delete all instances!")
        for instance in self.instances:
            status_code = await self.dcr_ar.delete_instance(self.graph_id,int(instance))
            if status_code == 204:
                print(f"[i] Successfully deleted instance with id: {instance}")
            else:
                print(f"[x] Failed to delete instance with id: {instance} status code: {status_code}")

        await self.show_instances_box()

def greeting(name):
    if name:
        return f"Hello, {name}"   
     
def main():
    return CloudApp()
