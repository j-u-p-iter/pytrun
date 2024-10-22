RED = "\033[91m"
GREEN = "\033[92m" 
RESET = "\033[0m" 

def cprint(text, status = '', padding_left = 0):
    message = None

    if status == 'success':
        message = f"{GREEN}{text}{RESET}"

    elif status == 'failure':
        message = f"{RED}{text}{RESET}"

    result_message = " " * padding_left + message

    print(result_message)
