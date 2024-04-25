
def alpha(word):
    if not word.replace(" ", "").isalpha():
        return False
    else:
        return True


def digit(word):
    if not word.isdigit():
        return False
    else:
        return True
