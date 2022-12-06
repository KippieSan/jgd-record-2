import constant as const
# <:icon-name:int>
BLU = const.BLU
COB = const.COB
EIE = const.EIE
EVI = const.EVI
ICE = const.ICE
KIP = const.KIP
KJU = const.KJU
KMR = const.KMR
MAS = const.MAS
MAT = const.MAT
MIL = const.MIL
NEO = const.NEO
PEL = const.PEL
RYO = const.RYO
RYU = const.RYU
SIM = const.SIM
SKR = const.SKR
SPA = const.SPA
SUK = const.SUK
UME = const.UME
YOG = const.YOG
AJI = const.AJI
SHO = const.SHO
JUN = const.JUN
MSC = const.MSC
DRI = const.DRI
ESP = const.ESP
CAZ = const.CAZ
UMI = const.UMI

ICON_DICT = {':Blu:': 0, ':Cob:': 1, ':Eie:': 2, ':Evi:': 3, ':Ice:': 4, ':Kip:': 5, ':Kju:': 6, ':Kmr:': 7, ':Mas:': 8, ':Mat:': 9,
             ':Mil:': 10, ':Neo:': 11, ':Pel:': 12, ':Ryo:': 13, ':Ryu:': 14, ':Sim:': 15, ':Skr:': 16, ':Spa:': 17, ':Suk:': 18, ':Ume:': 19,
             ':Yog:': 20, ':Aji:': 21, ':Sho:': 22, ':Jun:': 23, ':Msc:': 24, ':Dri:': 25, ':Esp:': 26, ':Caz:': 27, ':Umi:': 28}
ICON_LIST = [BLU, COB, EIE, EVI, ICE, KIP, KJU, KMR, MAS, MAT,
             MIL, NEO, PEL, RYO, RYU, SIM, SKR, SPA, SUK, UME,
             YOG, AJI, SHO, JUN, MSC, DRI, ESP, CAZ, UMI]

def icon_convert(player_icon: str):
    icon = ''
    start = False
    for c in player_icon:
        if not start and c == ':':
            icon += c
            start = True
        elif start and c != ':':
            icon += c
        elif start and c == ':':
            icon += c
            break
    return icon

# icon listからアイコンを出力できるようにして返す <:alias:num>
def get_icon(icon_list: str):
    new_icon_list = ''
    for i in icon_list.split():
        # ICON_LISTのインデックスの取得
        index = ICON_DICT[i]
        new_icon_list += ' <' + i + str(ICON_LIST[index]) + '>'
    return new_icon_list
