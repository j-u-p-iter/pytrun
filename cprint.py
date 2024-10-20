RED = "\033[91m"
GREEN = "\033[92m" 
RESET = "\033[0m" 

def cprint(text, status = ''):
    if status == 'success':
        return print(f"{GREEN}{text}{RESET}")

    elif status == 'failure':
        return print(f"{RED}{text}{RESET}")
