import communication


class Usb:
    def __init__(self, vid, pid, interface):
        self.vid = vid
        self.pid = pid
        self.interface = interface

    def send_bulk(self, endpoint, data):
        communication.Bulk(self.vid, self.pid, self.interface, endpoint).send(data)

    def receive_bulk(self, endpoint):
        return communication.Bulk(self.vid, self.pid, self.interface, endpoint).receive()


    def send_interrupt(self, endpoint, callback):
        interrupt = communication.Interrupt(self.vid, self.pid, self.interface, endpoint)
        interrupt.write_interrupt_handler(callback)

    def receive_interrupt(self, endpoint, callback):
        interrupt = communication.Interrupt(self.vid, self.pid, self.interface, endpoint)
        interrupt.read_interrupt_handler(callback)

    def send_control(self, endpoint, request, request_type, value, index, size, data):
        control = communication.Control(self.vid, self.pid, self.interface, endpoint)
        control.send(request, request_type, value, index, size, data)

    def receive_control(self, endpoint, request, request_type, value, index, size, data):
        control = communication.Control(self.vid, self.pid, self.interface, endpoint)
        control.receive(request, request_type, value, index, size, data)
