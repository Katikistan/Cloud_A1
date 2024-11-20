import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


def make_instance_box(self):
           
    instance_box = toga.Box(style=Pack(direction=COLUMN,flex=1))

    self.instance_details = toga.Label(
        text="Select an instance to view details.",
        style=Pack(padding=10))
        
    instance_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
    instance_box.add(self.instance_details)
        
    instance_box = toga.Box(style=Pack(direction=COLUMN,flex=1))
            
    role_items = list([' ', 'Doctor', 'Nurse', 'Patient'])
    selected_role_item = 'Doctor'
    events = [
        {'id': 'Diagnose', 'label': 'Diagnose', 'role': 'Doctor'},
        {'id': 'Operate', 'label': 'Operate', 'role': 'Doctor'},
        {'id': 'Give treatment', 'label': 'Give treatment', 'role': 'Nurse'},
        {'id': 'Take treatment', 'label': 'Take treatment', 'role': 'Patient'}
    ]

    instance_label = toga.Label("Each instance will appear here", style=Pack(padding=5))
    instance_box.add(instance_label)

    instance_row = toga.Box(style=Pack(direction=ROW, flex=1, padding=5))

    # Left Column
    role_column = toga.Box(style=Pack(direction=COLUMN, padding=5, flex=1))
    role_column.add(toga.Label("Current role:", style=Pack(padding=(0, 5))))
    role_column.add(toga.Label("Select other role:", style=Pack(padding=(0, 5))))
    self.role_selection = toga.Selection(
        items=role_items,
        value=role_items[0],
        on_change=self.role_changed,
        style=Pack(padding=(0, 5))
    )
    role_column.add(self.role_selection)

    # Right Column
    instance_column = toga.Box(style=Pack(direction=COLUMN, padding=5, alignment="top", flex=1))
    instance_column.add(toga.Label("Current instance:", style=Pack(padding=(0, 5))))
    instance_column.add(toga.Label("Not yet added!", style=Pack(padding=(0, 5))))

    instance_row.add(role_column)
    instance_row.add(instance_column)

    instance_box.add(instance_row)

    # scrollcontainer 
    event_container = toga.ScrollContainer(style=Pack(flex=1, padding=5))
    event_box = toga.Box(style=Pack(direction=COLUMN, alignment="top", padding=(0,5)))
    for event in events:
        event_button = toga.Button(
            text=f"{event['label']} (role: {event['role']})",
            id=event['id'],
            on_press=self.execute_event,
            style=Pack(padding=5)  
        )
        event_box.add(event_button)
    event_container.content = event_box
    instance_box.add(event_container)
    return instance_box
