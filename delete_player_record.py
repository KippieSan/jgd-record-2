import icon_constant as ic
"""
r!pdelete level-name, player-icon
r!pdelete level-name
"""
def command_divided(command: str):
    return command.split(',')
def delete_player_record(command: str, record: str):
    command_list = command_divided(command)
    level = ''
    icon = ''
    changed = False
    if len(command_list) == 2:
        level, icon = command_list
        icon = ic.icon_convert(icon)
    else:
        level = command_list[0]

    print(level + " " + icon)

    new_record = ''
    for level_data in record.splitlines():
        rlevel, rpos, ricon = level_data.split(',')
        if rlevel == level and icon == '':
            changed = True
        elif rlevel == level:
            if len(ricon.split()) == 1 and ricon.split()[0] == icon:
                changed = True
                continue
            new_record += (rlevel + ',' + rpos + ',')
            first = True
            for i in ricon.split():
                print(i + " " + icon)
                if i == icon:
                    changed = True
                elif first:
                    new_record += i
                    first = False
                else:
                    new_record += (' ' + i)
            new_record += '\n'
        elif ricon != '-':
            new_record += level_data + '\n'

    return [new_record, changed]
