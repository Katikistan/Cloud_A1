import httpx
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from helloworld.options.login_box import make_login_box
from helloworld.options.logout_box import make_logout_box
from helloworld.options.all_instances_box import make_all_instances_box
from helloworld.options.instance_box import make_instance_box
from helloworld.services.dcr_active_repository import check_login_from_dcr, DcrActiveRepository, DcrUser

class CloudApp(toga.App):

    def startup(self):
        login_box = make_login_box(self)
        all_instances_box = make_all_instances_box(self)
        instance_box = make_instance_box(self)
        logout_box = make_logout_box(self)

        
        self.option_container = toga.OptionContainer(
            content=[
                toga.OptionItem("Login", login_box),
                toga.OptionItem("All instances", all_instances_box),
                toga.OptionItem("Instance run", instance_box),
                toga.OptionItem("Logout", logout_box),
                ],
            on_select = self.option_item_changed,
            style=Pack(direction=COLUMN))

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.option_container
        self.option_container.content['Logout'].enabled = False
        self.option_container.content['All instances'].enabled = False
        self.option_container.content['Instance run'].enabled = False
        self.main_window.show()

    async def option_item_changed(self,widget):
        print('[i] You have selected another Option Item!')
        if widget.current_tab.text == 'All instances':
            await self.show_instances_box()


    async def login_handler(self, widget):
        connected = await check_login_from_dcr(self.username_input.value,self.password_input.value)
        if connected:
            self.dcr_user = DcrUser(self.username_input.value,self.password_input.value)
            self.dcr_ar = DcrActiveRepository(self.dcr_user)
            self.option_container.content['Logout'].enabled = True
            self.option_container.content['All instances'].enabled = True
            self.option_container.content['Instance run'].enabled = True

            self.option_container.curent_tab = 'All instances'
            
            self.option_container.content['Login'].enabled = False
            print(f"[i] You are logged in as {self.username_input.value}!")
        else:
            print(f"[x] Login failed!")

    async def logout_handler(self, widget):
        print("You want to logout!")
        self.option_container.content['Login'].enabled = True
        self.option_container.content['Logout'].enabled = False
        self.option_container.content['All instances'].enabled = False
        self.option_container.content['Instance run'].enabled = False
        self.option_container.current_tab = 'Login'
        self.username_input.value = None
        self.password_input.value = None

    async def role_changed(self, widget):
            self.selected_role_item = self.role_selection.value
            print(f"[i] You changed the role to {self.selected_role_item}!")
            
    async def execute_event(self, widget):
        print(f"[i] You want to execute event: {widget.id}")

    async def show_instance(self, widget):
            print(f"[i] You want to show {widget.id}")
            instance_id = widget.id

    async def show_instances_box(self):
        self.all_instances_box.clear()
        
        self.instances = {}        
        dcr_ar_instaces = await self.dcr_ar.get_instances(self.graph_id)
        if len(dcr_ar_instaces) > 0:
            self.instances = dcr_ar_instaces
        
        self.all_instances_box = toga.Box(style=Pack(direction=COLUMN,flex=1))

        all_instances_container = toga.ScrollContainer(
                horizontal=False, style=Pack(direction=COLUMN, flex=1)
            )       
            
        instances_box = toga.Box(style=Pack(direction=COLUMN))
        top_box = toga.Box(style=Pack(direction=COLUMN))
        
        create_instance_button = toga.Button(
            #instance['name'],
            "Create new instance",
            on_press=self.create_instance,
            style=Pack(padding=5)
            #id=instance['id']
            )
        top_box.add(create_instance_button)

        del_all_button = toga.Button(
            "Delete all instances",
            on_press=self.delete_all_by_id,
            style=Pack(padding=5, color="red")
                #id=f"X{instance['id']}"
        )
        top_box.add(del_all_button)

        for instance in self.instances:
            buttons_box = toga.Box(style=Pack(direction=ROW))
                
            instance_button = toga.Button(
                instance['name'],
                on_press=self.show_instance,
                style=Pack(padding=5),
                id=instance['id']
            )
            buttons_box.add(instance_button)
                
            del_button = toga.Button(
                "X",
                on_press=self.delete_instance_by_id,
                style=Pack(padding=5, color="red"),
                id=f"X{instance['id']}"
            )
            buttons_box.add(del_button)
                
            instances_box.add(buttons_box)

        all_instances_container.content = instances_box
            
        self.all_instances_box.add(top_box)
        self.all_instances_box.add(all_instances_container)


        self.all_instances_box.add(toga.Label("All instances", style=Pack(padding=5)))
        
        
        self.all_instances_box.refresh()
    
    
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
        print(f"[i] Create new instance!")

    async def delete_all_by_id(self, widget):
        print(f"[i] You want to delete all instances!")
        for instance in self.instances:
            status_code = await self.dcr_ar.delete_instance(self.graph_id,instance['id'])
            if status_code == 200:
                print(f"[i] Successfully deleted instance with id: {instance['id']}")
            else:
                print(f"[x] Failed to delete instance with id: {instance['id']} status code: {status_code}")
        await self.show_instances_box()

def greeting(name):
    if name:
        return f"Hello, {name}"   
     
def main():
    return CloudApp()
