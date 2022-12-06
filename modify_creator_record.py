import icon_constant as ic
"""
r!cmodify level-name, option, modified

option: LNAME CNAME CICON ID LINK
"""

def modify_creator_record(command: str, record: str):
    if len(command.split(',')) != 3:
        return [record, False, True]
    level, option, modified = command.split(',')
    option = option.split()[0]
    changed = False
    invalid_option = False
    new_record = ''
    for level_data in record.splitlines():
        rlevel, rcreator, ricon, rid, rlink = level_data.split(',')

        if rlevel == level:
            match option:
                case 'LNAME':
                    changed = True
                    new_record += modified + ',' + rcreator + ',' + ricon + ',' + rid + ',' + rlink + '\n'
                case 'CNAME':
                    changed = True
                    new_record += rlevel + ',' + modified + ',' + ricon + ',' + rid + ',' + rlink + '\n'
                case 'CICON':
                    changed = True
                    new_record += rlevel + ',' + rcreator + ',' + ic.icon_convert(modified) + ',' + rid + ',' + rlink + '\n'
                case 'ID':
                    changed = True
                    new_record += rlevel + ',' + rcreator + ',' + ricon + ',' + modified + ',' + rlink + '\n'
                case 'LINK':
                    changed = True
                    new_record += rlevel + ',' + rcreator + ',' + ricon + ',' + rid + ',' + modified + '\n'
                case _:
                    invalid_option = True
        else:
            new_record += level_data + '\n'
    return [new_record, changed, invalid_option]
