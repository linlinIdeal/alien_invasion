import platform

class GetPath():
    def __init__(self, path):
        if platform.system() == 'Windows':
            self.path = path.replace('\\', '/')
        else:
            self.path = path.replace('/', '\\')
        