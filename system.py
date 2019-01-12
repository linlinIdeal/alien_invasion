import platform

def real_path(path):
    if platform.system() == 'Windows':
        return path.replace('\\', '/')
    else:
        return path.replace('/', '\\')
        