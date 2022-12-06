import icon_constant as ic

def is_level_duplicated(level_name: str, pcstr: str):
    found_level, found = '', False
    for record in pcstr.splitlines():
        level = record.split(',')[0]
        if (level != level_name) and (level.upper() == level_name.upper()):
            found_level = level
            found = True

    return [found_level, found]

def is_level_exists(level_name: str, pcstr: str):
    found = False
    for record in pcstr.splitlines():
        level = record.split(',')[0]
        if level == level_name:
            found = True

    return found

def icon_exist(icon: str):
    if icon in ic.ICON_DICT:
        return True
    return False
