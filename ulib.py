import fcntl

class communication :

    def __init__(self, filename, mode):
        self.file = open(filename, mode)

    def recive(self):
        return self.file.read()

    def send(self, messege):
        self.file.write(messege)

    def close(self):
        self.file.close();

    def ioctl(self, operation):
        fcntl.ioctl(self.file, operation)



