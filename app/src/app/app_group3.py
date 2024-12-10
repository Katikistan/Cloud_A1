import httpx
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from options.login_box import make_login_box
from options.logout_box import make_logout_box
from options.all_instances_box import make_all_instances_box
from options.instance_box import make_instance_box
from services.dcr_active_repository_group3 import check_login_from_dcr, DcrActiveRepository, DcrUser, EventsFilter
from services import database_connection as dbc

from services.database_connection_group3 import (
    get_dcr_role,
    update_dcr_role,
    get_all_instances,
    get_instances_for_user,
    insert_instance,
    update_instance,
    delete_instance
)

class CloudApp(toga.App):
    graph_id = 1986525
    dcr_ar = None 

    def startup(self):
        self.login_box = make_login_box(self)
        self.instances = {}        
        self.all_instances_box = make_all_instances_box(self)
        self.instance_box = make_instance_box(self)
        self.logout_box = make_logout_box(self)

        
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
            self.user.role = dbc.get_dcr_role(email=self.user.email)
            self.dcr_ar = DcrActiveRepository(self.dcr_user)
            self.option_container.content['Logout'].enabled = True
            self.option_container.content['All instances'].enabled = True
            self.option_container.content['Instance run'].enabled = True
            # self.option_container.content['Login'].enabled = False 
            print(f'[i] Role: {self.user.role}')
            print(f"[i] You are logged in as {self.username_input.value}!")
        else:
            print(f"[x] Login failed!")

    async def logout_handler(self, widget):
        print("You want to logout!")
        self.username_input.value = None
        self.password_input.value = None
        self.option_container.current_tab = 'Login'
        self.option_container.content['Login'].enabled = True
        self.option_container.content['Logout'].enabled = False
        self.option_container.content['All instances'].enabled = False
        self.option_container.content['Instance run'].enabled = False
        

    async def role_changed(self, widget):
            self.selected_role_item = self.role_selection.value
            await update_dcr_role(self.email, self.selected_role_item)
            print(f"[i] You changed the role to {self.selected_role_item}!")
            
    async def execute_event(self, widget):
        event_id = widget.id
        status_code = await self.dcr_ar.execute_event(self.graph_id, self.current_instance_id, event_id)

        if status_code == 200:
            events = await self.dcr_ar.get_events(self.graph_id, self.current_instance_id, EventsFilter.PENDING)
            is_valid = len(events) == 0
            await update_instance(self.current_instance_id, is_valid)
            print(f"[i] Successfully executed event: {event_id}")
        else:
            print(f"[x] Failed to execute event: {event_id}")

    async def show_instance(self, widget):
        print(f"[i] You want to show {widget.id}")
        self.current_instance_id = widget.id
        self.option_container.current_tab = "Instance run"
        await self.show_instance_box()


    async def show_instances_box(self):
        self.all_instances_box.clear()
        
        self.instances = {}
        dcr_ar_instances = await self.dcr_ar.get_instances(self.graph_id)
        db_instances = await get_all_instances()
        user_instances = await get_instances_for_user(self.dcr_user.email) #til at lave my_instances
        
        #skal have instance id. bruges til at disable knapper der ikke tilhører brugeren!
        my_instances = [instance_id for instance_id, _ in user_instances] 

        #for loop hvor jeg tjekker om dcr ar instances er i databasen... lidt ligesom create  
        for instance in dcr_ar_instances:
            if any(db_instance[0] == instance for db_instance in db_instances):
                self.instances[instance] = f"Instance:{instance}"
        
        #DISABLE KNAPPER, brug my instances til kun at 
        for user_instance in user_instances:
            if any(user_instance in self.instances):
                pass 
        
        
        
        print(f"[i] Found {len(dcr_ar_instances)} instances")
        
        self.all_instances_box = make_all_instances_box(self)
        self.all_instances_box.refresh()
    
    
    async def delete_instance_by_id(self, widget):
        print(f"[i] You want to delete {widget.id[1:]}")
        instance_id = widget.id[1:]
        status_code = await self.dcr_ar.delete_instance(self.graph_id,instance_id)
        if status_code == 200:
            await delete_instance(instance_id) ###
            print(f"[i] Successfully deleted instance with id: {instance_id}")
        else:
            print(f"[x] Failed to delete instance with id: {instance_id} status code: {status_code}")
        await self.show_instances_box()
            
    async def create_instance(self,widget): ##################### IKKE DONE!!!!???? ########################
        self.current_instance_id = await self.dcr_ar.create_new_instance(self.graph_id)
        instances = await self.dcr_ar.get_instances(self.graph_id)
        instance = await self.dcr_ar.get_instances(self.graph_id)
        # if self.current_instance_id in instances
        # self.basic_auth[0] for at få email
        
        if any(instance['id'] == self.current_instance_id for instance in instances):
            await insert_instance(self.current_instance_id, True,self.basic_auth[0])
        else:
            await insert_instance(self.current_instance_id, False,self.basic_auth[0])
        
        self.option_container.current_tab = "Instance run"
        await self.show_instance_box()
        
    async def delete_all_by_id(self, widget):
        #skal bruge g_instances() fra dcr active repo, den siger "Get all active instances for a given graph id"
        #delete where instances[id]
        print(f"[i] You want to delete all instances!")
        instances = self.dcr_ar.get_instances(self.graph_id) ###
        for instance in instances:
            status_code = await self.dcr_ar.delete_instance(self.graph_id, instance['id'])
            if status_code == 200:
                await delete_instance(instance['id']) ###
                print(f"[i] Successfully deleted instance with id: {instance['id']}")
            else:
                print(f"[x] Failed to delete instance with id: {instance['id']} status code: {status_code}")
        await self.show_instances_box()

def greeting(name):
    if name:
        return f"Hello, {name}"   
     
def main():
    return CloudApp()
    