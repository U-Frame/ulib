import fcntl

class communication :

    def __init__(self, vid, pid):
	self.vid = vid
	self.pid = pid

    def recive(self):
        file = open(self.vid+"/"+self.pid, "r")
	data = file.read()
	file.close()
        return data

    def send(self, messege):
        file = open(self.vid+"/"+self.pid, "a")
        file.write(messege)
	file.close()

    def ioctl(self, operation):
        file = open(self.vid+"/"+self.pid, "r+")
        fcntl.ioctl(file, operation)
	file.close()

if __name__ == "__main__":
    como = communication("new", "new.txt")
    como.send("hello")
    print(como.recive())
