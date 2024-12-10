import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from app.services.dcr_active_repository import DcrActiveRepository, DcrEvent, DcrUser


async def make_instance_box(self):
    self.instance_box.clear()

    self.instance_details = toga.Label(
        text="Select an instance to view details.",
        style=Pack(padding=10))
        
    events = await self.dcr_ar.get_events(self.graph_id, self.current_instance_id)
    role_items = []
    if self.dcr_user.role:
        role_items.append(self.dcr_user.role)
    for event in events:
        event_role = event.role
        if event_role not in role_items:
            role_items.append(event_role)
        
    self.role_selection = toga.Selection(
        items=role_items,
        on_change=self.role_changed,
        style=Pack(padding=5)
    )
    if len(role_items)>0:
        self.role_selection.value = role_items[0]
        self.dcr_user.role = self.role_selection.value
    
    instance_label = toga.Label("Each instance will appear here", style=Pack(padding=5))
    self.instance_box.add(instance_label)

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

    self.instance_box.add(instance_row)

    print("hej!!!")
    # scrollcontainer 
    event_container = toga.ScrollContainer(style=Pack(flex=1, padding=5))
    event_box = toga.Box(style=Pack(direction=COLUMN, alignment="top", padding=(0,5)))
    for event in events:
        color = None
        btn_enabled = True
        text = event.label
        if event.enabled:
            color = "green"
        if event.pending:
            color = "blue"
            text = text + " !"
        if len(event.role)>0:
            if event.role != self.dcr_user.role:
                btn_enabled = False
            text = text + f" (role: {event.role})"
        if event.enabled:
            event_button = toga.Button(
                text=text,
                style=Pack(padding=5, color=color),
                id=event.id,
                on_press=btn_enabled
            )
            event_box.add(event_button)
    event_container.content = event_box
    self.instance_box.add(event_container)


    self.instance_box.add(toga.Label('Select an instance from All instances or Create new!'))
    self.instance_box.refresh()
