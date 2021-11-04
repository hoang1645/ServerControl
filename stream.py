from tkinter.constants import END
import cv2 
import numpy as np
from numpy.lib.ufunclike import fix
import pyautogui
import pickle
import struct

class StreamingSender():
    def __init__(self,conn=None,addr=None,x_reso=1024,y_reso=768):
        self.conn=conn
        self.addr=addr
        self.is_running=True
        self.x_res=x_reso
        self.y_res=y_reso
        self.__encoding_parameters = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    def start_stream(self):
        is_running=True
        while is_running:
            frame = self.get_frame()
            result, frame = cv2.imencode('.jpg', frame, self.__encoding_parameters)
            data = pickle.dumps(frame, 0)
            size = len(data)
            try:
                self.conn.sendall(struct.pack('>L', size) + data)
            except ConnectionResetError:
                is_running = False
            except ConnectionAbortedError:
                is_running = False
            except BrokenPipeError:
                is_running = False
        self.conn.close()
        cv2.destroyAllWindows()
    def get_frame(self):
        screen = pyautogui.screenshot()
        frame = np.array(screen)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.x_res, self.y_res), interpolation=cv2.INTER_AREA)
        return frame
class StreamingReciever():
    def __init__(self,conn=None,addr=None):
        self.conn=conn
        self.addr=addr
        self.is_running=True
    def show_stream(self):
        payload_size = struct.calcsize('>L')
        data = b""
        while self.is_running:

            break_loop = False

            while len(data) < payload_size:
                received = self.conn.recv(4096)
                if received == b'':
                    self.conn.close()
                    break_loop = True
                    break
                data += received

            if break_loop:
                break

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]

            msg_size = struct.unpack(">L", packed_msg_size)[0]

            while len(data) < msg_size:
                data += self.conn.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow("share screen", frame)
            if cv2.waitKey(1) == ord('q'):
                self.conn.close()
                break
        cv2.destroyAllWindows()