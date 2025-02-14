
WARNING = '\033[93m'
ERROR = '\033[91m'
SUCCESS = '\033[92m'
ENDC = '\033[0m'


def print_warning(message):
    print(WARNING + message + ENDC)


def print_error(message):
    print(ERROR + message + ENDC)


def print_success(message):
    print(SUCCESS + message + ENDC)
