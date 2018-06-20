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
        else:
            raise ValueError("Path does not exist")

    def send(self, data, size=0):
        file = open(self.path, "w")
        file.write(data,size)
        file.close()

    def device_control(self, byte_buffer, data, operation):
        for d in data:
            byte_buffer.append(d)
        temp_buffer = array.array("B", byte_buffer)
        buffer = array.array("c", temp_buffer.tostring())
        fcntl.ioctl(self.path, buffer, operation)
        return buffer[8:].tostring()

    def receive(self, size=0):
        file = open(self.path, "r")
        data = file.read(size)
        file.close()
        return data

    def ioctl


class Bulk(Communication):

    def __init__(self, vid, pid, interface, endpoint, endpoint_type="bulk"):
        self.path = "/home/sayed/dev/" + "/" + vid + "/" + pid + "/" + interface + "/" + endpoint_type + "/" + "{0:03}".format(
            endpoint)
        super().__init__(self.path)

    def send(self, data):
        super().send(data)

    def receive(self):
        return super().receive()


class Interrupt(Bulk):
    def __init__(self, vid, pid, interface, endpoint):
        super().__init__(vid, pid, interface, endpoint, "interrupt")
        structure = struct.pack("i", 0)
        node_file = open(self.path, "r")
        buffer = array.array("i", structure)
        operation = 0
        fcntl.ioctl(node_file, operation, buffer, 1)
        node_file.close()
        self.interrupt_interval = buffer[0]

    def write_interrupt_handler(self, callback_function=None):
        thread = threading.Thread(target=self.__write_interrupt_caller, args=(self.path, self.interrupt_interval
                                                                            , callback_function))
        thread.start()
        return thread

    def __write_interrupt_caller(self, callBack_function=None):
        while True:
            data = callBack_function()
            # self.writeInterrupt(len(data), self.path, data)
            self.send(data,self.size)
            time.sleep(self.interrupt_interval / 1000)

    def read_interrupt_handler(self, callback_function=None):
        thread = threading.Thread(target=self.__read_interrupt_caller, args=(self.path, self.interrupt_interval
                                                                           , callback_function))
        thread.start()
        return thread

    def __read_interrupt_caller(self, callback_function=None):
        while True:
            data = self.receive()
            callback_function(data)
            time.sleep(self.interrupt_interval / 1000.0)


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
        if request is not None:
            req = self.form_request_packet(request, request_type, value, index, size)
            messege = messege + str(req)
            messege = messege + data
        super().send(messege)

    def receive(self, request, request_type, value, index, size, data):
        if request is not None:
            byte_buffer = bytearray(self.form_request_packet(request, request_type, value, index, size))
            return super().device_control(self.path, byte_buffer, data, config.IOCTL_CONTROL_READ)


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
