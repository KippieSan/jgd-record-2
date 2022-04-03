import icon_constant as ic
"""
r!pcommit level-name, player-icon
r!pcommit level-name, player-icon -1

r!pcommit super greatest level 2, :Spa: :Neo: :Blu:
"""

def command_divided(command: str):
    command_list = command.split(',')
    return command_list

def commit_player_record(command: str, record: str):
    command_list = command_divided(command)
    level, icon = command_list
    out_of_range = False
    if len(icon.split()) == 2:
        icon = icon.split()[0]
        out_of_range = True

    icon = ic.icon_convert(icon)
    new_record = ''
    is_exist = False
    changed = False
    for level_data in record.splitlines():
        rlevel, rposition, ricons = level_data.split(',')
        if level == rlevel:
            if icon in ricons:
                is_exist = True
                new_record += level_data + '\n'
            if not is_exist:
                changed = True
                if ricons == '-':
                    new_record += rlevel + ',' + rposition + ',' + icon + '\n'
                else:
                    new_record += rlevel + ',' + rposition + ',' + ricons + ' ' + icon + '\n'
        elif ricons != '-':
            new_record += level_data + '\n'
    
    if not is_exist and out_of_range:
        changed = True
        new_record += level + ',-1,' + icon + '\n'
    return [new_record, is_exist, changed]