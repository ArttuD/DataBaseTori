import unittest
from classes.server_manager import Server_Manager
from tools.client_moc import client_moc
from multiprocessing import Process

def start_client():

    cm = client_moc()
    cm.pipe()
    
class TestEmploree(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def CreateServer_and_connect(self):

        server_host = Server_Manager("./bases/DataBase", True)
        res = server_host.open_socket()

        p = Process(target=start_client, args=(r'__30,first,Arttu,employees',))
        p.start()
        server_host.wait_clients()
        server_host.close_socket()
        p.join()

        self.assertEqual(res, 1)

    def log_in(self):
        

        


if __name__ == '__main__':
    unittest.main()