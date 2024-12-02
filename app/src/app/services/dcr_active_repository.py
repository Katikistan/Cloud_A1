import httpx
import xml.etree.ElementTree as ET

from typing import Optional

from enum import Enum

class EventsFilter(Enum):
    ALL = "all"
    ENABLED_OR_PENDING = "enabled-or-pending"
    ENABLED = "only-enabled"
    PENDING = "only-pending"

class DcrEvent(object):
    '''
    A class to represent a DcrEvent
    '''

    def __init__(self, 
                 id:int, 
                 label:str, 
                 enabled:bool=True, 
                 pending:bool=False, 
                 role:Optional[str]=None, 
                 sequence:Optional[int]=None) -> None:
        self.id = id
        self.label = label
        self.enabled = enabled
        self.pending = pending
        self.role = role
        self.sequence = sequence

class DcrUser(object):
    '''
    A class to represent a DcrUser with the same login credentials as for the dcr active repository
    '''

    def __init__(self, email:str, password:str, role:Optional[str]=None):
        self.email = email
        self.password = password
        self.role = role

def parse_event_from_xml(event_xml):
    event_id = event_xml.attrib['id']
    label = event_xml.attrib['label']
    enabled = True if event_xml.attrib['enabled'] == "true" else False
    pending = True if event_xml.attrib['pending'] == "true" else False
    role = event_xml.attrib['roles']
    sequence = int(event_xml.attrib['sequence'])
    return DcrEvent(event_id, label, enabled, pending, role, sequence)


class DcrActiveRepository(object):
    '''
    A class designed to interface with the online DCR Active repository.
    To fill in the class template URLs and the appropriate http call (get, put, post, delete) please use the DCR Active repository documentation:
    https://documentation.dcr.design/documentation/dcr-active-repository/

    You also have the swagger page for testing and reference: https://repository.dcrgraphs.net/index.html (we are only using hte DCRSimulator part)
    Alternatively to the swagger page you can use Postman as shown in the lecture slides.
    '''

    def __init__(self,dcr_user: DcrUser):
        #TODO store a tuple for the (username, password)
        self.basic_auth = (dcr_user.email, dcr_user.password)

    async def get_instances(self, graph_id):
        '''
        Get all active instances (or simulations) for a given graph id.
        '''
        url = f"https://repository.dcrgraphs.net/api/graphs/{graph_id}/sims" # this is the url you call (note: using f strings simplifies the insertion of the input parameters)
        instances = {} # this is a dictionary to store the resulting simulations
        async with httpx.AsyncClient() as client: # remember we're using an AsyncClinet()
            response = await client.get(url, auth=self.basic_auth) # always await the response. Here we need a GET http command.
            if response.text and len(response.text)>0: # now we do some checks
                root = ET.fromstring(response.text)
                for s in root.findall("trace"):
                    instances[s.attrib['id']] = "Instance:"+s.attrib['id'] # we parse the response value into our sims dictionary
        return instances # we return the dictionary of simulations

    async def create_new_instance(self, graph_id):
        '''
        Create a new instance (simulation) for a given graph id
        '''
        url = f"https://repository.dcrgraphs.net/api/graphs/{graph_id}/sims" #TODO: fill in the correct url
        async with httpx.AsyncClient() as client:
            response = await client.post(url, auth=self.basic_auth) #TODO: call the client with the apropriate http command. Remember the await in front and the auth as a parameter.
            return response.headers['simulationid'] # we return the simulation id

    async def delete_instance(self,graph_id,instance_id):
        url = f"https://repository.dcrgraphs.net/api/graphs/{graph_id}/sims/{instance_id}" #TODO: fill in the correct url
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, auth=self.basic_auth) #TODO: call the client with the apropriate http command. Remember the await in front and the auth as a parameter.
            return response.status_code
            
    async def execute_event(self,graph_id,instance_id,event_id):
        url = f"https://repository.dcrgraphs.net/api/graphs/{graph_id}/sims/{instance_id}/events/{event_id}" #TODO: fill in the correct url
        async with httpx.AsyncClient() as client:
            response =  await client.post(url, auth=self.basic_auth)  #TODO: call the client with the apropriate http command. Remember the await in front and the auth as a parameter.
            return response.status_code

    async def get_events(self, graph_id, instance_id, filter: EventsFilter = EventsFilter.ALL):
        url = f"https://repository.dcrgraphs.net/api/graphs/{graph_id}/sims/{instance_id}/events?filter={filter.value}" #TODO: fill in the correct url
        async with httpx.AsyncClient() as client:
            response = await client.get(url, auth=self.basic_auth) #TODO: call the client with the apropriate http command. 
            # Remember the await in front and the auth as a parameter here we get the list of events in the xml format from the response
            root = ET.fromstring(response.json()) # the .json() here is needed because there is a mistmatch in the expected result format between httpx and the dcr rest api. the response is xml.
            events_xml = root.findall('event')
            events = []
            for event_xml in events_xml:
                event = parse_event_from_xml(event_xml) # we parse the events from xml into the DcrEvent class.
                events.append(event)

            return events        

async def check_login_from_dcr(username, password):
    '''
    This is a simple test to check if we can login. 
    Technically it returns the list of graph ids but we're not using them.
    '''
    try: # a try catch block to prevent the app from crashing in case of errors
        url = "https://repository.dcrgraphs.net/api/graphs" # url to retrieve graph ids
        async with httpx.AsyncClient() as client:
            response = await client.get(url, auth=(username, password)) # this is where you pass your username and password
            if response.status_code == httpx.codes.OK: # check the status code to know we've been logged in
                return True # return True for success (2xx)
            else:
                return False # False if the status code is not ok (not 2xx)
    except Exception as e:
        print(f'[x] {e}')
        return False # in case the url is wrong or some other error we again return False


async def main():
    graph_id= # TODO: place your own graph id
    check_login = False
    while check_login == False:
        username = input("Enter you DCR portal username: ")
        from getpass import getpass
        password = getpass("Enter you DCR portal password: ")
        check_login = await check_login_from_dcr(username,password)
        if check_login == False:
            print(f"[x] Login failed try again!")
    if check_login == True:
        dcr_user = DcrUser(username,password)
        dcr_ar = DcrActiveRepository(dcr_user)
        sim_id = await dcr_ar.create_new_instance(graph_id)
        sim_ids = await dcr_ar.get_instances(graph_id)
        if sim_id in sim_ids.keys():
            print(f"[i] Found the newly created instance with id: {sim_id}")
            events = await dcr_ar.get_events(graph_id,sim_id,EventsFilter.ALL)
            for event in events:
                print(f"[i] Found event with label: {event.label} (id {event.id}, enabled {event.enabled}, pending {event.pending}, role {event.role if event.role else 'None'})")
            stop = False
            while len(events)>0 and not stop:
                event_to_execute_label = input("Type the event label to execute (or type stop): ")
                if event_to_execute_label.lower() == "stop":
                    stop = True
                else:
                    event_to_execute = None
                    for event in events:
                        if event.label.lower() == event_to_execute_label.lower():
                            event_to_execute = event
                    if event_to_execute is not None:
                        execute_event_status_code = await dcr_ar.execute_event(graph_id,sim_id,event_to_execute.id)
                        if httpx.codes.is_success(execute_event_status_code):
                            print(f"[i] Successfully executed event: {event_to_execute.label}")
                        new_events = await dcr_ar.get_events(graph_id,sim_id,EventsFilter.ALL)
                        print(f"[i] After executing event {event_to_execute.label} with id {event_to_execute.id}")
                        for event in new_events:
                            print(f"[i] Found event with label: {event.label} (id {event.id}, enabled {event.enabled}, pending {event.pending}, role {event.role if event.role else 'None'})")     
                        events = new_events
            deleted_instance_status_code = await dcr_ar.delete_instance(graph_id,sim_id)
            if httpx.codes.is_success(deleted_instance_status_code):
                print(f"[i] Successfully deleted instance with id: {sim_id}")
            else:
                print(f"[x] Failed to delete instance with id: {sim_id} status code: {deleted_instance_status_code}")
        else:
            print(f"[x] Did not find the newly created instance with id: {sim_id}")
        # clean up any rogue instances
        sim_ids = await dcr_ar.get_instances(graph_id)
        if len(sim_ids)>0:
            print(f'[i] Deleting any rogue instances. Please wait!')
        for inst_id in sim_ids:
             await dcr_ar.delete_instance(graph_id,inst_id)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())