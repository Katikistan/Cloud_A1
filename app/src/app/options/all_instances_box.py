import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


def make_all_instances_box(self):
    all_instances_box = toga.Box(style=Pack(direction=COLUMN,flex=1))

    all_instances_container = toga.ScrollContainer(
            horizontal=False, style=Pack(direction=COLUMN, flex=1)
        )       
        
    instances_box = toga.Box(style=Pack(direction=COLUMN))
    top_box = toga.Box(style=Pack(direction=COLUMN))


    self.instances = [
        {'id': 1, 'name': 'Instance 1'},
        {'id': 2, 'name': 'Instance 2'},
        {'id': 3, 'name': 'Instance 3'}
    ]        
        
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
        
    all_instances_box.add(top_box)
    all_instances_box.add(all_instances_container)
    return all_instances_box
        