import icon_constant as ic
"""
r!c

crecordを次の形式で受け取る
level-name,creator-name,creator-icon,level-id,[youtube-link]

次のListのListを作成して返す
[ level-name, creator-name, creator-icon, level-id, youtube-link, has-link ]
"""

def get_creator_record(crecord: str):
    record_list = []
    for record in crecord.splitlines():
        level, creator, icon, id, link = record.split(',')
        icon = ic.get_icon(icon)
        has_link = True
        if link == '-':
            has_link = False
        record_list.append([ level, creator, icon, id, link, has_link ])
    return record_list