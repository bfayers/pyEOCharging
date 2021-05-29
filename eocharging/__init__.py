from eocharging.Manager import Manager


def connection(username=None, password=None):
    if username is None:
        raise Exception("No username provided")
    if password is None:
        raise Exception("No password provided")
    return Manager(username=username, password=password)
