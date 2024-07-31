import io
import json
import selectors
import struct
import sys

request_search = {
    "morpheus": "Follow the white rabbit. \U0001f430",
    "ring": "In the caves beneath the Misty Mountains. \U0001f48d",
    "\U0001f436": "\U0001f43e Playing ball! \U0001f3d0",
}


class Message:

    def __init__(self, selector, sock, addr):

        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_buffer = b""
        self._send_buffer = b""
        self._jsonheader_len = None
        self.jsonheader = None
        self.request = None
        self.response_created = False
        self.msg_received = None

        self.buffer_size = 4096
        self.msg_write = None

    def _set_selector_events_mask(self, mode):

        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {mode!r}.")
        
        self.selector.modify(self.sock, events, data=self)

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
            return 1, self.msg_received
        if mask & selectors.EVENT_WRITE:

            return self.write(), []

    def read(self):
        #oPen message
        self._read()

        if self._jsonheader_len is None:
            self.process_protoheader()
            
        if self._jsonheader_len is not None:
            if self.jsonheader is None:
                self.process_jsonheader()

        if self.jsonheader:
            if self.request is None:
                self.process_request()

    def _read(self):
        try:
            # Should be ready to read
            data = self.sock.recv(self.buffer_size)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            print("Package temporary blocked", BlockingIOError)
            pass
        else:
            if data:
                self._recv_buffer += data
            else:
                raise RuntimeError("Peer closed.")
            
    def process_protoheader(self):
        #Receive and unpack json header size of 2-by, remove it from the buffer
        #indicates the length of json header
        hdrlen = 2
        if len(self._recv_buffer) >= hdrlen:
            self._jsonheader_len = struct.unpack(
                ">H", self._recv_buffer[:hdrlen]
            )[0]
            self._recv_buffer = self._recv_buffer[hdrlen:]

    def process_jsonheader(self):
        #Check the length of the package, decode, remove, and check that package is okay 
        hdrlen = self._jsonheader_len
        if len(self._recv_buffer) >= hdrlen:
            self.jsonheader = self._json_decode(
                self._recv_buffer[:hdrlen], "utf-8"
            )
            self._recv_buffer = self._recv_buffer[hdrlen:]

            for reqhdr in (
                "byteorder",
                "content-length",
                "content-type",
                "content-encoding",
            ):
                if reqhdr not in self.jsonheader:
                    raise ValueError(f"Missing required header '{reqhdr}'.")
                
    def _json_decode(self, json_bytes, encoding):
        #Decode data package into json header into dictionary
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        
        obj = json.load(tiow)
        tiow.close()

        return obj

    def process_request(self):

        #Save content, remove, decode data, and act accordingly
        content_len = self.jsonheader["content-length"]
        if not len(self._recv_buffer) >= content_len:
            return
        
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]

        if self.jsonheader["content-type"] == "text/json":

            encoding = self.jsonheader["content-encoding"]
            self.request = self._json_decode(data, encoding)
            print(f"Received request {self.request!r} from {self.addr}")
        else:
            # Binary or unknown content-type
            encoding = self.jsonheader["content-encoding"]
            self.request = data
            print(
                f"Received {self.jsonheader['content-type']} "
                f"request from {self.addr}"
            )
            self.msg_received = self.request.decode("utf-8").split("__")[1:]
        

        # Set selector to listen for write events, we're done reading.
        self._set_selector_events_mask("w")  

    def write(self):

        if self.msg_write:
        #if self.request:
            if not self.response_created:
                self.create_response()

        return self._write()  

    def create_response(self):

        if self.jsonheader["content-type"] == "text/json":
            response = self._create_response_json_content()
        else:
            # Binary or unknown content-type
            response = self._create_response_binary_content()

        message = self._create_message(**response)
        self.response_created = True
        self._send_buffer += message

    def _create_response_json_content(self):
        action = self.request.get("action")

        if action == "search":
            query = self.request.get("value")
            answer = request_search.get(query) or f"No match for '{query}'."
            content = {"result": answer}
        else:
            content = {"result": f"Error: invalid action '{action}'."}

        content_encoding = "utf-8"

        response = {
            "content_bytes": self._json_encode(content, content_encoding),
            "content_type": "text/json",
            "content_encoding": content_encoding,
        }
        return response

    def _create_response_binary_content(self):
        response = {
            "content_bytes": bytes(self.respo, encoding="utf-8"),
            "content_type": "binary/custom-server-binary-type",
            "content_encoding": "binary",
        }
        return response
    
    def _create_message(
        self, *, content_bytes, content_type, content_encoding
    ):
        jsonheader = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
        }

        jsonheader_bytes = self._json_encode(jsonheader, "utf-8")
        message_hdr = struct.pack(">H", len(jsonheader_bytes))
        message = message_hdr + jsonheader_bytes + content_bytes

        return message
    
    def _json_encode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)
    
    def _write(self):

        if self._send_buffer:

            print(f"Sending {self._send_buffer!r} to {self.addr}")
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                print("Resource temporarily unavailable (errno EWOULDBLOCK)")
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]
                # Close when the buffer is drained. The response has been sent.
                if sent and not self._send_buffer:
                    return self.close()
    def close(self):
            print(f"Closing connection to {self.addr}")
            try:
                self.selector.unregister(self.sock)
            except Exception as e:
                print(
                    f"Error: selector.unregister() exception for "
                    f"{self.addr}: {e!r}"
                )

            try:
                self.sock.close()
            except OSError as e:
                print(f"Error: socket.close() exception for {self.addr}: {e!r}")
            finally:
                # Delete reference to socket object for garbage collection
                self.sock = None
                return -1

if __name__ == "__main__":

    #open socket
    host_socket = Message()
