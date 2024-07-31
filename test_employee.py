import unittest
from classes.employee import Employee

class TestEmploree(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.emp = Employee("first", "last", "status", "project", "starting", "phone_number")

    def test_create_emp(self):

        result = self.emp.fullname
        self.assertEqual(result, "first last")


if __name__ == '__main__':
    unittest.main()