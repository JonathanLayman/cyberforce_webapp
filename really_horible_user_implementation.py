user_db = {
    'bob': 'sjhd76eww!',
    'clem': 'khsd54#h',
    'alicia': 'jhsjhsd222!',
    'sue': '76shshs63!',
    'plank': '5!ys!hhsds'
}


def auth_user(username, password):
    try:
        if user_db[username] == password:
            return True
        else:
            return False
    except KeyError:
        return False
