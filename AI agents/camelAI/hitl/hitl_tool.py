def ask_user_input(prompt: str, default: str = None):
    """ asks user the quetion and gives answer """
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    user_input = input(prompt)
    return user_input.strip() or default