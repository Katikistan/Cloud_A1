import unittest
from database_connection_group3 import (
    db_connect,
    get_dcr_role,
    update_dcr_role,
    get_all_instances,
    get_instances_for_user,
    insert_instance,
    update_instance,
    delete_instance
)


class TestDatabaseConnection(unittest.TestCase):

    def setUp(self):
        """Setup database connection before each test."""
        self.connection = db_connect()
        self.cursor = self.connection.cursor(buffered=True)
        self.test_email = "zwx366@alumni.ku.dk"
        self.test_instance_id = 1
        self.test_role = "patient"

    def tearDown(self):
        """Clean up after each test."""
        self.cursor.close()
        self.connection.close()

    # Test for get_dcr_role
    def test_get_dcr_role(self):
        self.cursor.execute(
            "INSERT INTO DCRUsers (Email, Role) VALUES (%s, %s) ON DUPLICATE KEY UPDATE Role=%s",
            (self.test_email, self.test_role, self.test_role)
        )
        self.connection.commit()

        role = get_dcr_role(self.test_email)
        self.assertEqual(role, self.test_role)

    # Test for update_dcr_role
    def test_update_dcr_role(self):
        new_role = "UpdatedTestRole"
        update_dcr_role(self.test_email, new_role)
        role = get_dcr_role(self.test_email)
        self.assertEqual(role, new_role)

    # Test for get_all_instances
    def test_get_all_instances(self):
        insert_instance(self.test_instance_id, True, self.test_email)
        instances = get_all_instances()
        self.assertTrue(any(inst[0] == self.test_instance_id for inst in instances))

    # Test for get_instances_for_user
    def test_get_instances_for_user(self):
        insert_instance(self.test_instance_id, True, self.test_email)
        instances = get_instances_for_user(self.test_email)
        self.assertTrue(any(inst[0] == self.test_instance_id for inst in instances))

    # Test for insert_instance
    def test_insert_instance(self):
        insert_instance(self.test_instance_id, False, self.test_email)
        instances = get_instances_for_user(self.test_email)
        self.assertTrue(any(inst[0] == self.test_instance_id for inst in instances))

    # Test for update_instance
    def test_update_instance(self):
        insert_instance(self.test_instance_id, False, self.test_email)
        update_instance(self.test_instance_id, True)
        instances = get_instances_for_user(self.test_email)
        self.assertTrue(any(inst[1] == 1 for inst in instances))

    # Test for delete_instance
    def test_delete_instance(self):
        insert_instance(self.test_instance_id, True, self.test_email)
        delete_instance(self.test_instance_id)
        instances = get_instances_for_user(self.test_email)
        self.assertFalse(any(inst[0] == self.test_instance_id for inst in instances))


if __name__ == "__main__":
    unittest.main()
