import config
import fcntl
from bitarray import bitarray
import os
import struct
import array
import threading
import time
from helper import Helper


class Communication:
    def __init__(self, path):
        if os.path.exists(path):
            self.path = path
            buffer = array.array(struct.pack("iiiii", 0, 0, 0, 0, 0))
            buffer = self.device_control(0, buffer)
            self.type = buffer[0]
            self.direction = buffer[1]
            self.endpoint_address = buffer[2]
            self.interval = buffer[3]
            self.buffer_size = buffer[4]
        else:
            raise ValueError("Path does not exist")

    def send(self, data):
        file = open(self.path, "w")
        file.write(data)
        file.close()

    def receive(self, size=0):
        file = open(self.path, "r")
        data = file.read(size)
        file.close()
        return data

    def device_control(self, operation, buffer):
        file = open(self.path, "r")
        fcntl.ioctl(file, buffer, operation)
        file.close()
        return buffer


class Bulk(Communication):
    def __init__(self, vid, pid, interface, endpoint, endpoint_type="Bulk"):
        self.path = "/home/sayed/dev/" + "/" + vid + "/" + pid + "/" + interface + "/" + endpoint_type + "/" + "{0:03}".format(
            endpoint)
        super().__init__(self.path)


class Interrupt(Bulk):
    def __init__(self, vid, pid, interface, endpoint):
        super().__init__(vid, pid, interface, endpoint, "Interrupt")

    def write_interrupt_handler(self, callback_function=None):
        thread = threading.Thread(target=self.__write_interrupt_caller, args=(self.path, self.interval, callback_function))
        thread.start()
        return thread

    def __write_interrupt_caller(self, callback_function=None):
        while True:
            data = callback_function()
            self.send(data)
            time.sleep(self.interval / 1000.0)

    def read_interrupt_handler(self, callback_function=None):
        thread = threading.Thread(target=self.__read_interrupt_caller, args=callback_function)
        thread.start()
        return thread

    def __read_interrupt_caller(self, callback_function=None):
        while True:
            data = self.receive()
            callback_function(data)
            time.sleep(self.interval / 1000.0)


class Control(Communication):
    def __init__(self, vid, pid, interface, endpoint):
        self.path = "/home/sayed/dev/" + "/" + vid + "/" + pid + "/" + interface + "/" + "control" + "/" + "{0:03}".format(
            endpoint)
        super().__init__(self.path)

    def form_request_packet(self, request, request_type, value, index, size):

        return bitarray(
            "{0:08b}".format(request) + "{0:08b}".format(request_type) + "{0:<016b}".format(value) +
            "{0:<016b}".format(index) + "{0:<016b}".format(size)).tobytes()

    def send(self, request, request_type, value, index, size, data):
        messege = ""
        req = self.form_request_packet(request, request_type, value, index, size)
        messege = messege + str(req)
        messege = messege + data
        super().send(messege)

    def receive(self, request, request_type, value, index, size, data):
        buffer = array.array(struct.pack("ccHHH{width}s".format(width=size), request, request_type, value, index, size, data))
        return super().device_control(1, buffer)[8:]


if __name__ == '__main__':
    pass
# bulk_object = Bulk(vid="10", pid="10", interface="15", endpoint=config.BULK, node=config.OUT15)
# bulk_object.send("sayed")
# bulk_object = Bulk(vid="10", pid="10", interface="15", endpoint=config.BULK, node=config.OUT11)
# bulk_object.send("sayed")
# bulk_object = Bulk(vid="10", pid="10", interface="15", endpoint=config.BULK, node=config.IN10)
# interrupt_object = Interrupt(vid="10", pid="10", interface="15", endpoint=config.BULK, node=config.OUT15)
# interrupt_object.write_interrupt_handler(callback_function=callback2)
# interrupt_object = Interrupt(vid="10", pid="10", interface="15", endpoint=config.BULK, node=config.IN10)
# print(interrupt_object.read_interrupt_caller(callback_function=callback2))
