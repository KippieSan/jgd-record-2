
"""
player-recordとdemonlistを受け取ってdemonlistを更新する
"""

def update_list(demonlist: str, precord: str):
    list_data = demonlist.splitlines()
    record_data = precord.splitlines()

    rindex = 0
    new_list = ''
    for i in range(len(list_data)):
        added = False
        for j in range(len(record_data)):
            # i番目のレベルにレコードが存在するかを走査し、存在するならば追加する
            rlevel, _, ricons = record_data[j].split(',')
            list_level, list_pos, _ = list_data[i].split(',')

            if(rlevel == list_level):
                new_list += list_level + ',' + list_pos + ',' + ricons + '\n'
                added = True
            pass
        if not added:
            new_list += list_data[i] + '\n'
    
    for precord in record_data:
        # 圏外組を追加する
        _, position, _ = precord.split(',')
        pos = int(position)
        if pos == -1:
            new_list += precord + '\n'
    
    return new_list