from .wait import timeout


@timeout(seconds=5)
def get_message(data):
    if data.isnumeric():
        return data
