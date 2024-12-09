from mysql.connector import connect
import mysql

db_password = 'Gr3LMO2024'
sql_query_template = {}
sql_query_template['get_dcr_role'] = f"""SELECT Role FROM DCRUsers WHERE
Email = %(email)s"""
#TODO: fill in these templates with the right SQL query
# Get DCR Role for a specific user
# Get DCR Role for a specific user
sql_query_template['get_dcr_role'] = f"""
SELECT Role 
FROM DCRUsers 
WHERE Email = %(email)s;
"""

# Update DCR Role for a user
sql_query_template['update_dcr_role'] = f"""
UPDATE DCRUsers 
SET Role = %(role)s 
WHERE Email = %(email)s;
"""

# Get all instances with a JOIN
sql_query_template['get_all_instances'] = f"""
SELECT i.InstanceID, i.IsInValidState, ui.Email
FROM Instances i
INNER JOIN UserInstances ui ON i.InstanceID = ui.InstanceID;
"""

# Get instances linked to a specific user
sql_query_template['get_instances_for_user'] = f"""
SELECT i.InstanceID, i.IsInValidState
FROM Instances i
INNER JOIN UserInstances ui ON i.InstanceID = ui.InstanceID
WHERE ui.Email = %(email)s;
"""

# Insert a new instance into Instances table
sql_query_template['insert_instance'] = f"""
INSERT INTO Instances (InstanceID, IsInValidState) 
VALUES (%(id)s, %(valid)s)
ON DUPLICATE KEY UPDATE IsInValidState = %(valid)s;
"""

# Link a user to an instance in UserInstances table
sql_query_template['insert_instance_for_user'] = f"""
INSERT IGNORE INTO UserInstances (Email, InstanceID) 
VALUES (%(email)s, %(id)s);
"""

# Update an instance’s state
sql_query_template['update_instance'] = f"""
UPDATE Instances 
SET IsInValidState = %(valid)s 
WHERE InstanceID = %(id)s;
"""

# Delete an instance from the user-instances relationship
sql_query_template['delete_instance_from_user_instance'] = f"""
DELETE FROM UserInstances 
WHERE InstanceID = %(id)s;
"""

# Delete an instance completely
sql_query_template['delete_instance'] = f"""
DELETE FROM Instances 
WHERE InstanceID = %(id)s;
"""

def db_connect():
    from pathlib import Path
    resources_folder = Path(__file__).parent.resolve()
    cert_filepath = str(resources_folder.joinpath("DigiCertGlobalRootCA.crt.pem"))
    cnx = mysql.connector.connect(user="Group3", 
                                  password=db_password, 
                                  host="group32024.mysql.database.azure.com",
                                  port=3306, 
                                  database="tasklistdatabase3", 
                                  ssl_ca=cert_filepath)
    print(f'[i] cnx is connected: {cnx.is_connected()}')
    return cnx

def get_dcr_role(email):
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(sql_query_template['get_dcr_role'], {'email':email})
        query_result = cursor.fetchone()[0]
        cursor.close()
        cnx.close()
        return query_result
    except Exception as ex:
        print(f'[x] error get_dcr_role! {ex}')
        return None

def update_dcr_role(email,role):
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(sql_query_template['update_dcr_role'], 
                       {'role':role, 'email':email}, multi=False)
        cnx.commit()
        cursor.close()
        cnx.close()
    except Exception as ex:
        print(f'[x] error update_dcr_role! {ex}')
        
def get_all_instances():
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(sql_query_template['get_all_instances'])
        query_result = cursor.fetchall()
        cursor.close()
        cnx.close()
        return query_result
    except Exception as ex:
        print(f'[x] error get_all_instances! {ex}')
        return None

def get_instances_for_user(email):
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(sql_query_template['get_instances_for_user'], 
                       {'email':email})
        query_result = cursor.fetchall()
        cursor.close()
        cnx.close()
        return query_result
    except Exception as ex:
        print(f'[x] error get_instances_for_user! {ex}')
        return None
    
def insert_instance(id, valid, email):
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(sql_query_template['insert_instance'], 
                       {'id':id,'valid':valid}, multi=False) 
        cursor.execute(sql_query_template['insert_instance_for_user'], 
                       {'email':email,'id':id}, multi=False)
        cnx.commit()
        cursor.close()
        cnx.close()
    except Exception as ex:
        # Validate the instance_id
        print(id, valid, email)
        print(f'[x] error insert_instance! {ex}')
        
def update_instance(id, valid):
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(sql_query_template['update_instance'], 
                       {'id':id,'valid':valid}, multi=False)
        cnx.commit()
        cursor.close()
        cnx.close()
    except Exception as ex:
        print(f'[x] error update_instance! {ex}')
        
def delete_instance(id):
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        
        cursor.execute(sql_query_template['delete_instance_from_user_instance'],
        {'id':id}, multi=False)
        cursor.execute(sql_query_template['delete_instance'], {'id':id},
        multi=False)
        cnx.commit()
        cursor.close()
        cnx.close()
    except Exception as ex:
        print(f'[x] error delete_instance! {ex}')
        
        
####### TEST FRA CHATTEN, FIX TING ########
""" 
# Sample input dictionary
input_dict = {'email': 'zwx366@alumni.ku.dk', 'role': 'Patient'}

# Execute the query using cursor.execute
cnx = db_connect()
cursor = cnx.cursor(buffered=True)
cursor.execute(sql_query_template['get_dcr_role'], input_dict)
result = cursor.fetchone()
print("User Role:", result)

input_dict = {
    'instance_id': 101,
    'is_valid_state': True
}

# Insert the instance
cursor.execute(sql_query_template['insert_instance'], input_dict)
connection = db_connect()
connection.commit()
print("Instance inserted successfully.")
 """