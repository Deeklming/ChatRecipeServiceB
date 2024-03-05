from config import r

def login_required(name: str):
    if r.get(name):
        return True
    else:
        return False
