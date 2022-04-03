"""
r!cdelete level-name
"""

def delete_creator_record(command: str, record: str):
    level_name = command
    new_record = ''
    deleted = False
    for level_data in record.splitlines():
        level, _, _, _, _ = level_data.split(',')
        if level_name == level:
            deleted = True
        else:
            new_record += level_data + '\n'
    return [ new_record, deleted ]