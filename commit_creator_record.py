
import icon_constant as ic
"""
r!ccommit level-name, creator-name, creator-icon, ID, [video-link]
"""

def commit_creator_record(command: str, record: str):
    new_record = record
    found = True
    #print(new_record)
    command_list = command.split(',')
    # linkを含む
    if len(command_list) == 5:
        level, creator, icon, id, link = command_list
        new_record += level + ',' + creator + ',' + ic.icon_convert(icon) + ',' + id + ',' + link + '\n'
    # linkを含まない追加
    elif len(command_list) == 4:
        level, creator, icon, id = command_list
        new_record += level + ',' + creator + ',' + ic.icon_convert(icon) + ',' + id + ',-' + '\n'
    # 既存のレベルへのリンクの追加
    elif len(command_list) == 2:
        found = False
        level, link = command_list
        new_record = ''
        for level_data in record.splitlines():
            rlevel, rcreator, ricon, rid, _ = level_data.split(',')
            if rlevel == level:
                found = True
                new_record += rlevel + ',' + rcreator + ',' + ic.icon_convert(ricon) + ',' + rid + ',' + link + '\n'
            else:
                new_record += level_data + '\n'

    return [ new_record, found ]
