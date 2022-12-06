from typing import List
import icon_constant as ic
import constant as const
"""
r!ccommit level-name, creator-name, creator-icon, ID, [video-link], [after]
"""

def commit_creator_record(command_list: List[str], record: str):
    new_record_list = ''
    new_record = ''
    # print(new_record)
    level, creator, icon, id, link, after = command_list
    # linkを含む
    if link != const.Defstr:
        new_record += level + ',' + creator + ',' + ic.icon_convert(icon) + ',' + id + ',' + link
    # linkを含まない追加
    else:
        new_record += level + ',' + creator + ',' + ic.icon_convert(icon) + ',' + id + ',-'

    for level_data in record.splitlines():
        # afterと名前が同じレベルがあればこの直後にレコードを挿入
        level_name = level_data.split(',')[0]
        if after == level_name:
            new_record_list += level_data + '\n'
            new_record_list += new_record + '\n'
        else:
            new_record_list += level_data + '\n'
    # afterがデフォルト値であるならばリストの最後に追加する
    if after == const.Defstr:
        new_record_list += new_record + '\n'

    return new_record_list
