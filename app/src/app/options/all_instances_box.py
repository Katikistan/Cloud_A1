import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


async def make_all_instances_box(self):
    #all_instances_box = toga.Box(style=Pack(direction=COLUMN,flex=1))

    self.all_instances_box.clear()
        
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
        #id=['id']
        )
    top_box.add(create_instance_button)

    del_all_button = toga.Button(
        "Delete all instances",
        on_press=self.delete_all_by_id,
        style=Pack(padding=5, color="red")
        #id=f"X{instance['id']}"
    )
    top_box.add(del_all_button)

    self.instances = {}        
    dcr_ar_instances = await self.dcr_ar.get_instances(self.graph_id)
    print(f"[i] Found {len(dcr_ar_instances)} instances")

    if len(dcr_ar_instances) > 0:
        self.instances = dcr_ar_instances

    for instance_id, instance_name in self.instances.items():
  
        buttons_box = toga.Box(style=Pack(direction=ROW))
            
        instance_button = toga.Button(
            text=instance_name,
            on_press=self.show_instance,
            style=Pack(padding=5),
            id=instance_id
        )
        buttons_box.add(instance_button)
            
        del_button = toga.Button(
            "X",
            on_press=self.delete_instance_by_id,
            style=Pack(padding=5, color="red"),
            id=f"X{instance_id}"
        )

        buttons_box.add(del_button)
            
        instances_box.add(buttons_box)

    all_instances_container.content = instances_box
        
    self.all_instances_box.add(top_box)
    self.all_instances_box.add(all_instances_container)
        
    self.all_instances_box.refresh()

        