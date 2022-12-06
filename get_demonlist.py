from pointercratepy import Client

client = Client()

def demonlist():
    now = 0
    demonlist = ''

    while True:
        demons = client.get_demons(limit=100, after=now)
        if demons == []:
            break

        for demon in demons:
            demonlist += ','.join([str(demon.get("name")), str(demon.get("position")), '-']) + '\n'

        now += 100
    return demonlist
