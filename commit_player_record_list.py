import commit_player_record as cp
def commit_player_record_list(command: str, record: str):
    command_list = command.split(',')
    level_list, icon = command_list[:-1], command_list[-1]

    new_record = record
    player_exists = []
    not_changed = []

    for level in level_list:
        if level[0] == ' ':
            level = level[1:]
        new_command = level + ',' + icon
        new_record, is_exist, changed = cp.commit_player_record(new_command, new_record)

        if is_exist:
            player_exists.append(level)
        elif not changed:
            not_changed.append(level)
    
    return [new_record, player_exists, not_changed]

