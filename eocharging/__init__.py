from eocharging.Manager import Manager


def connection(username=None, password=None, access_token=None):
    if username is None and access_token is None:
        raise Exception("No username provided")
    if password is None and access_token is None:
        raise Exception("No password provided")
    return Manager(username=username, password=password, access_token=access_token)
