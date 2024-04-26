
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


def birthdate(date):
    if digit(date) and len(date) == 8:
        if int(date[0:2]) < 13 and int(date[2:4]) < 32 and int(date[4:8]) > 1900:
            return True
        else:
            return False
    else:
        return False
