#!/usr/bin/env python3

import selectors
import socket
import sys
import traceback

from tools.client_msg_moc import Message
sel = selectors.DefaultSelector()


class client_moc():

    def __init__(self, msg):

        self.host= '127.0.0.1'
        self.port = 65432
        self.action = 'binary'
        self.value = msg  #r'__30,first,Arttu,employees' 

        
    def create_request(self,action, value):
        if action == "search":
            return dict(
                type="text/json",
                encoding="utf-8",
                content=dict(action=action, value=value),
            )
        else:
            return dict(
                type="binary/custom-client-binary-type",
                encoding="binary",
                content=bytes(action + value, encoding="utf-8"),
            )


    def start_connection(self, host, port, request):

        addr = (host, port)

        print(f"Starting connection to {addr}")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = Message(sel, sock, addr, request)
        sel.register(sock, events, data=message)

    def pipe(self):

        request = self.create_request(self.action, self.value)
        self.start_connection(self.host, self.port, request)

        #wait for data
        try:
            while True:
                print("Waiting asnwer")
                events = sel.select(timeout=None)

                for key, mask in events:
                    message = key.data
                    try:
                        message.process_events(mask)
                    except Exception:
                        print(
                            f"Main: Error: Exception for {message.addr}:\n"
                            f"{traceback.format_exc()}"
                        )
                        message.close()
                # Check for a socket being monitored to continue.
                if not sel.get_map():
                    break

        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            sel.close()
