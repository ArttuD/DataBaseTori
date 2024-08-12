
import socket
import sys
import selectors
import types
import time

from classes.message import Message
from classes.database_manager import DataBaseManager

class Server_Manager():

    def __init__(self, file_path, debug_flag, host ="127.0.0.1" , port= 65432 ):

        self.HOST = host
        self.PORT = port
        self.sel = selectors.DefaultSelector()
        #try:
        self.db_m = DataBaseManager(file_path, debug_flag)
        #except:
        #    print("Cannot open database")

    def open_socket(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((self.HOST, self.PORT))

            print(f"Listening on {(self.HOST, self.PORT)}")

            return 1
        except:
            return - 1
        
    def accept_wrapper(self, sock):

        conn, addr = sock.accept()
        print(f"Accepted connection from {addr}")

        conn.setblocking(False)
        message = Message(self.sel, conn, addr)
        self.sel.register(conn, selectors.EVENT_READ, data=message)

    def wait_clients(self):

        self.recv_msg = [1, []]
        self.s.listen()
        self.s.setblocking(False)
        self.sel.register(self.s, selectors.EVENT_READ, data=None)
        try:
            while True:
                events = self.sel.select(timeout=1)
                
                for key, mask in events:
                    if key.data == None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        msg = key.data
                        try:
                            self.recv_msg = msg.process_events(mask)
                            
                            if self.recv_msg[0] == -1:
                                break

                            self.reply = self.process_msg(self.recv_msg[1])

                        except Exception:
                            print(
                                f"Main: Error: Exception for {msg.addr}:\n"
                                f"{msg.format_exc()}"
                            )
                            msg.close()

                if self.recv_msg[0] == -1:
                    break
        except KeyboardInterrupt:
            print("KB interrupt")
        finally:
            print("closing")
            self.sel.close()

    def close_socket(self):
        self.s.close()

    def vis_tables(self):
        print(self.db_m.print_table("employees"))
        print(self.db_m.print_table("orders"))

    def process_msg(self, msg):

        msg = "".join(msg)
        parts = msg.split(",")
        parts_ = list(parts[0])
        parts = parts[1:]

        #0 - refers to employee table
        #1 - refers to orders table
        self.act = int(parts_[0])
        self.target_table = int(parts_[1])


        if self.act == 0:
            #insertion
            if self.target_table == 0:
                if len(parts) == 6:
                    return self.db_m.insert_emp(parts)
                else:
                    return -1
            elif self.target_table == 1:
                if len(parts) == 17:
                    return self.db_m.insert_product(parts)
                else:
                    return -1
        elif self.act == 1:
            #modification
            if self.target_table == 0:
                if len(parts) == 5:
                    return self.db_m.update_emp(parts)
                else:
                    return -1
            elif self.target_table == 1:
                if len(parts) == 4:
                    return self.db_m.update_orders(parts)
                else:
                    return -1
        elif self.act == 2:
            #deletion
            if self.target_table == 2:
                if len(parts) == 17:
                    return self.db_m.remove_emp(parts)
                else:
                    return -1
            elif self.target_table == 1:
                if len(parts) == 1:
                    return self.db_m.remove_product(parts)
                else:
                    return -1
        elif self.act == 3:
            #visualize
            print("visualize")
            if self.target_table == 0:
                if len(parts) == 3:
                    print("fetching things from database")
                    return self.db_m.get_record(*parts)
                else:
                    return -1
            elif self.target_table == 1:

                if len(parts) == 3:
                    return self.db_m.get_record(*parts)
                else:
                    return -1
        else:
            print("uncrecognized command")
            return -1




if __name__ == "__main__":

    #open socket
    print(sys.argv)
    
    host_socket = Server_Manager("./bases/DataBase", True)
    ret = host_socket.open_socket()
    host_socket.wait_clients()
    host_socket.close_socket()

    print(ret)



"""
def service_connection(self, key, mask):

    sock = key.fileobj
    data = key.data

    if mask & self.sel.EVENT_READ:
        msg = self.s.recv(1024)
        if msg:
            print(f"Received {msg!r} from connection {msg.connid}")
            data.recv_total += len(msg)   
        if not msg or data.recv_total == data.msg_total:
            print(f"Closing connection to {data.addr}")
            self.sel.unregister(sock)
            sock.close()

    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)

        if data.outb:
            print(f"Sending {data.outb!r} to connection {data.connid}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]
"""





