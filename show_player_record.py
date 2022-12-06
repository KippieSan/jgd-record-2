import icon_constant as ic
LIMIT = 2000
MAX = 100000000
def divide_under_limit(record: str, cur: int):
    if len(record) <= LIMIT:
        return ([record], len(record))
    record_list = []
    tmp = ''
    for line in record.splitlines():
        if len(tmp) + len(line) + cur > LIMIT:
            record_list.append(tmp)
            tmp = (line + '\n')
            cur = 0
        else:
            tmp += (line + '\n')
    record_list.append(tmp)
    return (record_list, len(tmp))

def get_player_record(precord: str):
    header_list = [
        '__**Main List**__\n\n',
        '__**Extended List**__\n\n',
        '__**Legacy List**__\n\n',
        '__**圏外**__\n\n'
    ]
    main_passed = False
    extended_passed = False
    legacy_passed = False
    main = header_list[0]
    extended = header_list[1]
    legacy = header_list[2]
    other = header_list[3]

    for list_data in precord.splitlines():
        level, position, icons = list_data.split(',')
        pos = int(position)
        picon = '-'
        if icons != '-':
            picon = ic.get_icon(icons)
        else:
            continue

        if not main_passed and pos > 75:
            main_passed = True
        elif not extended_passed and pos > 150:
            extended_passed = True
        elif not legacy_passed and pos == -1:
            legacy_passed = True

        if not main_passed:
            main += (level + picon + '\n')
        elif not extended_passed:
            extended += (level + picon + '\n')
        elif not legacy_passed:
            legacy += (level + picon + '\n')
        else:
            other += (level + picon + '\n')

    main += '\n'
    extended += '\n'
    legacy += '\n'
    other += '\n'

    main_list, lm = divide_under_limit(main, 0)
    extended_list, le = divide_under_limit(extended, lm)
    legacy_list, ll = divide_under_limit(legacy, le)
    other_list, _ = divide_under_limit(other, ll)

    return [main_list, extended_list, legacy_list, other_list]
