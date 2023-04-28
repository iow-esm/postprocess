import fcntl
import os 

class CreateLockedFile:
    def __init__(self, file_name, mode="w", delete=True):
        self.file = None
        try:
            self.file= open(file_name, mode)
        except:
            raise Exception("File " +file_name+" locked!")

        fcntl.flock(self.file.fileno(), fcntl.LOCK_EX)

        self.file_name = file_name
        self.delete = delete

    def unlock(self):

        if self.file is None:
            return
        
        fcntl.flock(self.file.fileno(), fcntl.LOCK_UN)
        self.file.close()

        if self.delete:
            os.remove(self.file_name)

    def __del__(self):
        self.unlock()