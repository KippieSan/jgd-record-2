import discord
import discord.app_commands
import enum
import constant as const
import update_demonlist as updatec
import commit_player_record as pcommitc
import commit_player_record_list as plcommitc
import commit_creator_record as ccommitc
import delete_player_record as pdeletec
import delete_creator_record as cdeletec
import show_player_record as pc
import show_creator_record as cc
import modify_creator_record as cmodifyc
import icon_constant as icc
import get_demonlist as get
import check_duplicaion as dup

# チャンネルID
DEMONLIST = const.DEMONLIST
PRECORD = const.PRECORD
CRECORD = const.CRECORD

TOKEN = const.TOKEN

PPATH = const.PPATH
CPATH = const.CPATH
DPATH = const.DPATH
AVATAR = const.AVATAR

dstr = ''
pstr = ''
cstr = ''

client = discord.Client(intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    print("Active")
    # with open(AVATAR, 'rb') as f:
    # ____await client.user.edit(username=str('JGD Records'), avatar=f.read())
    # チャンネルの設定
    demonlist_data = client.get_channel(DEMONLIST)
    precord_data = client.get_channel(PRECORD)
    crecord_data = client.get_channel(CRECORD)
    # レコードデータのあるメッセージのID取得
    did = demonlist_data.last_message_id
    pid = precord_data.last_message_id
    cid = crecord_data.last_message_id
    # 実際のメッセージの取得
    demonlist = await demonlist_data.fetch_message(did)
    precord = await precord_data.fetch_message(pid)
    crecord = await crecord_data.fetch_message(cid)
    # メッセージからtxt byteデータの取得
    dbyte_data = await demonlist.attachments[0].read()
    pbyte_data = await precord.attachments[0].read()
    cbyte_data = await crecord.attachments[0].read()
    # byteデータをstrに変換
    global dstr
    global cstr
    dstr = dbyte_data.decode()
    pstr_data = pbyte_data.decode()
    cstr = cbyte_data.decode()
    # リストを更新
    global pstr
    pstr = updatec.update_list(dstr, pstr_data)
    await tree.sync()
    # print(pstr)
    # print(cstr)
    print("Initialization Completed\n")


@tree.command(name='p', description='player-recordsを表示します.')
async def p(ctx: discord.Interaction):
    await ctx.response.send_message('>>> player-recordを表示します.')
    global pstr
    record_list = pc.get_player_record(pstr)
    for list in record_list:
        for record in list:
            await ctx.channel.send('>>> ' + record)
    await ctx.delete_original_response()


@tree.command(name='c', description='creator-recordsを表示します.')
async def c(ctx: discord.Interaction):
    await ctx.response.send_message('>>> creator-recordを表示します.')
    global cstr
    record_list = cc.get_creator_record(cstr)
    for creator_record in record_list:
        msg = '>>> ***' + creator_record[0] + '*** by ' + creator_record[1] + ' ' + creator_record[2] + '\n'
        msg += 'ID: ' + creator_record[3] + '\n'
        if creator_record[5] is True:
            msg += '<' + creator_record[4].strip() + '>\n'
        await ctx.channel.send(msg)
    await ctx.channel.send('\n>>> 総作品数: {}'.format(len(record_list)))
    await ctx.delete_original_response()


class Color(enum.Enum):
    Red = enum.auto()
    Green = enum.auto()


class DuplicatedLevel(discord.ui.View):
    message: discord.InteractionMessage

    def __init__(self, level: str, icon: str, is_listed: bool):
        super().__init__()

        self.add_item(Button(Color.Red, 'キャンセル', 'cancel', level, icon, is_listed))
        self.add_item(Button(Color.Green, '追加する', 'add', level, icon, is_listed))
        self.timeout = 10.0

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)


class Button(discord.ui.Button):
    level = ''
    icon = ''
    is_listed = True

    def __init__(self, color: Color, label: str, custom_id: str, level: str, icon: str, is_listed: bool):
        super().__init__(
            style=discord.ButtonStyle.red if color == Color.Red else discord.ButtonStyle.green,
            label=label,
            custom_id=custom_id
        )
        self.level = level
        self.icon = icon
        self.is_listed = is_listed

    async def callback(self, interaction: discord.Interaction):
        if self.custom_id == 'cancel':
            await interaction.response.send_message('>>> キャンセルしました.')
            return
        else:
            await interaction.response.send_message('>>> player-recordsにレコードを追加します.')
            global pstr
            global dstr
            # print(self.level, self.icon, self.is_listed)
            new_precord, is_exist, changed = pcommitc.commit_player_record([self.level, self.icon, self.is_listed], pstr)
            # print(new_precord)
            precord_data = client.get_channel(PRECORD)
            with open(PPATH, "w") as record_file:
                record_file.write(new_precord)
            await precord_data.send(file=discord.File(PPATH))
            if is_exist:
                await interaction.followup.send(">>> プレイヤーは既に追加されています.")
            elif not changed:
                await interaction.followup.send(">>> 指定されたレベルはリスト上に存在しません. **圏外であれば`is_listed`をFalseに設定してください.**")
            else:
                pstr = updatec.update_list(dstr, new_precord)
                await interaction.followup.send(">>> レコードを更新しました.")
            await interaction.delete_original_response()
            return


@tree.command(name='pcommit', description='player-recordsにレコードを追加します.')
@discord.app_commands.describe(
    level='レコードに追加するレベルの名前.',
    icon='レコードに追加するプレイヤーのアイコン(:Kip:など).',
    is_listed='レコードに追加するレベルがDemonlistに載っているか(デフォルトはTrue).'
)
async def pcommit(ctx: discord.Interaction, level: str, icon: str, is_listed: bool = True):
    await ctx.response.send_message(">>> player-recordsにレコードを追加します.")
    global pstr
    global dstr
    # check permission
    if ctx.permissions.manage_messages is not True:
        await ctx.followup.send(">>> **このコマンドはヘルパー以上の役職を持っていないと使うことはできません.**")
        return
    # check icon form is correct
    converted = icc.icon_convert(icon)
    if not (len(converted) == 5 and converted[0] == ':' and converted[-1] == ':' and converted[1].isupper() and converted[2].islower() and converted[3].islower()):
        await ctx.followup.send(">>> **アイコンは**`:Aaa:`**の形式で送信してください.** 送信されたアイコン -> `" + icc.icon_convert(icon) + '`')
        return
    # check icon existence
    if not dup.icon_exist(converted):
        await ctx.followup.send(f">>> アイコン**{converted}**は存在しません. 入力しなおしてください.")
        ctx.delete_original_response()
        return
    # check level duplication
    duplicated_level, level_found = dup.is_level_duplicated(level, pstr)
    view = DuplicatedLevel(level=level, icon=icon, is_listed=is_listed)
    if level_found:
        view.message = await ctx.followup.send(
            content=f">>> 似た名前のレベル**{duplicated_level}**が既にレコードに追加されています. このまま追加しますか？\n( 追加しようとしたレベル: **{level}** )",
            view=view
        )
        return

    new_precord, is_exist, changed = pcommitc.commit_player_record([level, icon, is_listed], pstr)
    # print(new_precord)
    precord_data = client.get_channel(PRECORD)
    with open(PPATH, "w") as record_file:
        record_file.write(new_precord)
    await precord_data.send(file=discord.File(PPATH))
    if is_exist:
        await ctx.followup.send(">>> プレイヤーは既に追加されています.")
    elif not changed:
        await ctx.followup.send(">>> 指定されたレベルはリスト上に存在しません. **圏外であれば`is_listed`をFalseに設定してください.**")
    else:
        pstr = updatec.update_list(dstr, new_precord)
        await ctx.followup.send(">>> レコードを更新しました.")


@tree.command(name='pdelete', description='player-recordsからレコードを削除します.')
@discord.app_commands.describe(
    level='レコードから削除するレベルの名前.',
    icon='[オプション] 特定のプレイヤーのみを削除する場合, そのプレイヤーのアイコン.'
)
async def pdelete(ctx: discord.Interaction, level: str, icon: str = 'None'):
    await ctx.response.send_message(">>> player-recordsからレコードを削除します.")
    global pstr
    global dstr
    if ctx.permissions.manage_messages is not True:
        await ctx.followup.send(">>> **このコマンドはヘルパー以上の役職を持っていないと使うことはできません.**")
        return
    new_precord, changed = pdeletec.delete_player_record(','.join([level, icon]), pstr)
    precord_data = client.get_channel(PRECORD)
    with open(PPATH, "w") as record_file:
        record_file.write(new_precord)
    if not changed:
        await ctx.followup.send(">>> 該当のレベルもしくはプレイヤーは存在しません")
    else:
        pstr = updatec.update_list(dstr, new_precord)
        await precord_data.send(file=discord.File(PPATH))
        await ctx.followup.send(">>> レコードを更新しました")


@tree.command(name='ccommit', description='creator-recordsにレコードを追加します.')
@discord.app_commands.describe(
    level='レコードに追加するレベルの名前.',
    creator='レコードに追加するレベルのクリエイター.',
    icon='クリエイターのアイコン.',
    id='レコードに追加されるレベルのID',
    link='[オプション] レコードに追加されるレベルの動画へのリンク.',
    insert_after='[オプション] ここに入力されたレベルの直後にこのレコードを追加します.'
)
async def ccommit(ctx: discord.Interaction, level: str, creator: str, icon: str, id: int, link: str = const.Defstr, insert_after: str = const.Defstr):
    await ctx.response.send_message(">>> creator-recordsにレコードを追加します.")
    global cstr
    if ctx.permissions.manage_messages is not True:
        await ctx.followup.send(">>> **このコマンドはヘルパー以上の役職を持っていないと使うことはできません.**")
        return
    converted = icc.icon_convert(icon)
    if not (len(converted) == 5 and converted[0] == ':' and converted[-1] == ':' and converted[1].isupper() and converted[2].islower() and converted[3].islower()):
        await ctx.followup.send(">>> **アイコンは**`:Aaa:`**の形式で送信してください.** 送信されたアイコン -> `" + icc.icon_convert(icon) + '`')
        return
    # check icon existence
    if not dup.icon_exist(converted):
        await ctx.followup.send(f">>> アイコン**{converted}**は存在しません. 入力しなおしてください.")
        await ctx.delete_original_response()
        return
    # after初期値でないとき, afterが存在するか. 存在しない場合処理を終了する
    if insert_after != const.Defstr and not dup.is_level_exists(insert_after, cstr):
        await ctx.followup.send(f">>> レベル**{insert_after}**は存在しません. 入力しなおしてください.")
        await ctx.delete_original_response()
        return
    new_crecord = ccommitc.commit_creator_record([level, creator, icon, str(id), link, insert_after], cstr)
    crecord_data = client.get_channel(CRECORD)
    with open(CPATH, "w") as record_file:
        record_file.write(new_crecord)

    await ctx.followup.send(">>> レコードを更新しました.")
    await crecord_data.send(file=discord.File(CPATH))
    cstr = new_crecord


@tree.command(name='cdelete', description='creator-recordsからレコードを削除します.')
@discord.app_commands.describe(
    level='レコードから削除するレベルの名前.'
)
async def cdelete(ctx: discord.Interaction, level: str):
    await ctx.response.send_message(">>> creator-recordsからレコードを削除します.")
    global cstr
    if ctx.permissions.manage_messages is not True:
        await ctx.followup.send(">>> **このコマンドはヘルパー以上の役職を持っていないと使うことはできません.**")
        return
    new_crecord, deleted = cdeletec.delete_creator_record(level, cstr)
    crecord_data = client.get_channel(CRECORD)
    with open(CPATH, "w") as record_file:
        record_file.write(new_crecord)
    await crecord_data.send(file=discord.File(CPATH))
    if deleted:
        await ctx.followup.send(">>> レコードを更新しました.")
        cstr = new_crecord
    else:
        await ctx.followup.send(">>> 該当のレベルは存在しません.")


class Options(enum.Enum):
    LevelName = 'LNAME'
    CreatorName = 'CNAME'
    CreatorIcon = 'CICON'
    ID = 'ID'
    VideoLink = 'LINK'


@tree.command(name='cmodify', description='creator-recordsの情報を編集します.')
@discord.app_commands.describe(
    level='レコードを編集するレベルの名前.',
    option='オプションの選択 (LNAME(Level Name), CNAME(Creator Name), CICON(Creator Icon), ID, LINK).',
    modified='編集された情報.'
)
async def cmodify(ctx: discord.Interaction, level: str, option: Options, modified: str):
    await ctx.response.send_message(">>> creator-recordsの情報を編集します.")
    global cstr
    if ctx.permissions.manage_messages is not True:
        await ctx.followup.send(">>> **このコマンドはヘルパー以上の役職を持っていないと使うことはできません.**")
        return
    if option == Options.CreatorIcon:
        converted = icc.icon_convert(modified)
        if not (len(converted) == 5 and converted[0] == ':' and converted[-1] == ':' and converted[1].isupper() and converted[2].islower() and converted[3].islower()):
            await ctx.followup.send(">>> **アイコンは**`:Aaa:`**の形式で送信してください.** 送信されたアイコン -> `" + icc.icon_convert(modified) + '`')
            return
    new_crecord, changed, invalid_option = cmodifyc.modify_creator_record(','.join([level, option.value, modified]), cstr)
    crecord_data = client.get_channel(CRECORD)
    if invalid_option:
        await ctx.followup.send(">>> オプションが無効です。(使用可能オプション: 'LNAME' 'CNAME', 'CICON', 'ID', 'LINK').")
    elif not changed:
        await ctx.followup.send(">>> 該当のレベルは存在しません.")
    else:
        with open(CPATH, "w") as record_file:
            record_file.write(new_crecord)
        await crecord_data.send(file=discord.File(CPATH))
        await ctx.followup.send(">>> レコードを更新しました.")
        cstr = new_crecord


@tree.command(name='plcommit', description='player-recordsをリスト形式で追加します.')
@discord.app_commands.describe(
    levellist='レコードに追加するレベルのカンマ(,)区切りのリスト(level1, level2, ... ).',
    icon='レコードに追加するプレイヤーのアイコン(:Kip:など).'
)
async def plcommit(ctx: discord.Interaction, levellist: str, icon: str):
    await ctx.response.send_message(">>> player-recordsをリスト形式で追加します.")
    global pstr
    global dstr
    if ctx.permissions.manage_messages is not True:
        await ctx.followup.send(">>> **このコマンドはヘルパー以上の役職を持っていないと使うことはできません.**")
        return
    converted = icc.icon_convert(icon)
    if not (len(converted) == 5 and converted[0] == ':' and converted[-1] == ':' and converted[1].isupper() and converted[2].islower() and converted[3].islower()):
        await ctx.followup.send(">>> **アイコンは**`:Aaa:`**の形式で送信してください.** 送信されたアイコン -> `" + icc.icon_convert(icon) + '`')
        return
    new_precord, player_exists, not_changed = plcommitc.commit_player_record_list(levellist + ',' + icon, pstr)
    precord_data = client.get_channel(PRECORD)
    with open(PPATH, "w") as record_file:
        record_file.write(new_precord)
    await precord_data.send(file=discord.File(PPATH))
    # 既に追加されているレベルの表示
    if len(player_exists) != 0:
        await ctx.followup.send(">>> 以下のレベルについてプレイヤーは既に追加されています.")
        player_exists_level_list = ''
        for level in player_exists:
            player_exists_level_list += level + ' '
        await ctx.followup.send(">>> " + player_exists_level_list + "\n")
    # リストに存在しないレベルの表示
    if len(not_changed) != 0:
        await ctx.followup.send(">>> 以下のレベルはリストに存在しません. リスト内であればレベル名の確認, 圏外であれば各個'pcommit'を使ってレコードを追加してください.")
        levels_not_exist_on_list = ''
        for level in not_changed:
            levels_not_exist_on_list += level + ' '
        await ctx.followup.send(">>> " + levels_not_exist_on_list + "\n")
    # リストの更新
    pstr = updatec.update_list(dstr, new_precord)
    await ctx.followup.send(">>> レコードを更新しました.")


@tree.command(name='update', description='Demonlistをアップデートします.')
async def update(ctx: discord.Interaction):
    await ctx.response.send_message(">>> Demonlistをアップデートします.")
    if ctx.permissions.manage_messages is not True:
        await ctx.followup.send(">>> **このコマンドはヘルパー以上の役職を持っていないと使うことはできません.**")
        return

    precord_data = client.get_channel(PRECORD)
    pid = precord_data.last_message_id
    precord = await precord_data.fetch_message(pid)
    pbyte_data = await precord.attachments[0].read()

    dstr = get.demonlist()
    pstr = pbyte_data.decode()
    pstr = updatec.update_list(dstr, pstr)
    demonlist_channel = client.get_channel(DEMONLIST)
    with open(DPATH, "w") as record_file:
        record_file.write(dstr)
    await demonlist_channel.send(file=discord.File(DPATH))
    # print(pstr)
    await ctx.followup.send(">>> Demonlistをアップデートしました.")
    await ctx.delete_original_response()


@tree.command(name='purge', description='指定数のメッセージを削除します.')
@discord.app_commands.describe(
    n='削除するメッセージの数.'
)
async def purge(ctx: discord.Interaction, n: int):
    await ctx.response.send_message(">>> {}件のメッセージを削除します.".format(n))
    if ctx.permissions.manage_messages is not True:
        await ctx.followup.send(">>> **このコマンドはヘルパー以上の役職を持っていないと使うことはできません.**")
        return
    deleted = await ctx.channel.purge(limit=n)
    await ctx.followup.send((">>> メッセージを{}件削除しました.".format(len(deleted))))
    # await ctx.delete_original_response()


client.run(TOKEN)
