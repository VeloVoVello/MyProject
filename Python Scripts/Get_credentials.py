import getpass

def get_credentials():
    username = input('Username: ')
    password = None
    while not password:
        password = getpass.getpass(prompt='Password: ')
        password_verify = getpass.getpass(prompt='Retype your password: ')
        if password != password_verify:
            print('Passwords do not match. Try again.')
            password = None
    return username, password

username, password = get_credentials()