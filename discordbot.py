import discord
import update_demonlist as update
import commit_player_record as pcommit
import commit_creator_record as ccommit
import delete_player_record as pdelete
import delete_creator_record as cdelete
import show_player_record as p
import show_creator_record as c
import modify_creator_record as cmodify
import const

# チャンネルID
DEMONLIST = const.DEMONLIST_ID
PRECORD = const.PRECORD_ID
CRECORD = const.CRECORD_ID

TOKEN = const.TOKEN

PPATH = const.PPATH
CPATH = const.CPATH
AVATAR = const.AVATAR
PAR = const.PAR

dstr = ''
pstr = ''
cstr = ''

client = discord.Client()


@client.event
async def on_ready():
    print("Active")
    #with open(AVATAR, 'rb') as f:
        #await client.user.edit(username=str('JGD Records'), avatar=f.read())
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
    dstr      = dbyte_data.decode()
    pstr_data = pbyte_data.decode()
    cstr      = cbyte_data.decode()
    # リストを更新
    global pstr
    pstr = update.update_list(dstr, pstr_data)
    print(pstr)
    print(cstr)
    print("Initialization Completed\n")
    pass


@client.event
async def on_message(message):
    global dstr
    global pstr
    global cstr
    # メッセージの取得とprefixの取得
    msg = message.content
    prefix = msg[:2]
    # メッセージを送ったユーザーのロール
    roles = message.author.roles
    permi = roles[-1].permissions
    # チャンネルの設定
    precord_data = client.get_channel(PRECORD)
    crecord_data = client.get_channel(CRECORD)
    # botからの送信をはじく
    if message.author.bot:
        return
    # prefixがr!ならコマンド
    if prefix == 'r!':
        # prefix以降最初のコマンド r!pcommitのpcommitなど
        command = msg[2:].split()
        # commandで分岐
        match(command[0]):
            # 'p': プレイヤーレコード表示
            case 'p':
                record_list = p.get_player_record(pstr)
                for list in record_list:
                    for record in list:
                        await message.channel.send('>>> '+ record)

            # 'pcommit': レコード追加
            case 'pcommit':
                if permi.manage_channels != True:
                    await message.channel.send(">>> **このコマンドはヘルパー以上の役職を持っていないと使うことはできません**")
                    return
                new_precord, is_exist, changed = pcommit.commit_player_record(msg[len('r!pcommit '):], pstr)
                # print(new_precord)
                with open(PPATH, "w") as record_file:
                    record_file.write(new_precord)
                await precord_data.send(file=discord.File(PPATH))
                if is_exist:
                    await message.channel.send(">>> プレイヤーは既に追加されています")
                elif not changed:
                    await message.channel.send(">>> 指定されたレベルはリスト上に存在しません。圏外であれば`-1`オプションを付けてください")
                else:
                    pstr = update.update_list(dstr, new_precord)
                    await message.channel.send(">>> レコードを更新しました")

            # 'pdelete': レコード削除
            case 'pdelete':
                if permi.manage_channels != True:
                    await message.channel.send(">>> **このコマンドはヘルパー以上の役職を持っていないと使うことはできません**")
                    return
                new_precord, changed = pdelete.delete_player_record(msg[len('r!pdelete '):], pstr)
                with open(PPATH, "w") as record_file:
                    record_file.write(new_precord)
                if not changed:
                    await message.channel.send(">>> 該当のレベルもしくはプレイヤーは存在しません")
                else:
                    pstr = update.update_list(dstr, new_precord)
                    await precord_data.send(file=discord.File(PPATH))
                    await message.channel.send(">>> レコードを更新しました")

            # 'c': クリエイターレコード表示
            case 'c':
                record_list = c.get_creator_record(cstr)
                embed=discord.Embed(
                    title='Creators Record List',
                    color=0x00ff00,
                )
                for record in record_list:
                    level, creator, icon, id, link, has_link = record
                    if has_link:
                        embed.add_field(
                            name=(PAR + level + ' By ' + creator + ' ' + icon),
                            value=('ID: ' + id + '\n' + link),
                            inline=False
                        )
                    else:
                        embed.add_field(
                            name=(PAR + level + ' By ' + creator + ' ' + icon),
                            value=('ID: ' + id),
                            inline=False
                        )
                await message.channel.send(embed=embed)
            
            # 'ccommit': レコードの追加
            case 'ccommit':
                if permi.manage_channels != True:
                    await message.channel.send(">>> **このコマンドはヘルパー以上の役職を持っていないと使うことはできません**")
                    return
                new_crecord, found = ccommit.commit_creator_record(msg[len('r!ccommit '):], cstr)
                with open(CPATH, "w") as record_file:
                    record_file.write(new_crecord)
                if not found:
                    await message.channel.send(">>> 該当のレベルは存在しません")
                else:
                    await message.channel.send(">>> レコードを更新しました")
                    await crecord_data.send(file=discord.File(CPATH))
                    cstr = new_crecord
            
            # 'cdelete': レコードの削除
            case 'cdelete':
                if permi.manage_channels != True:
                    await message.channel.send(">>> **このコマンドはヘルパー以上の役職を持っていないと使うことはできません**")
                    return
                new_crecord, deleted = cdelete.delete_creator_record(msg[len('r!cdelete '):], cstr)
                with open(CPATH, "w") as record_file:
                    record_file.write(new_crecord)
                await crecord_data.send(file=discord.File(CPATH))
                if deleted:
                    await message.channel.send(">>> レコードを更新しました")
                    cstr = new_crecord
                else:
                    await message.channel.send(">>> 該当のレベルは存在しません")
            
            # 'cmodify': レコードの編集
            case 'cmodify':
                if permi.manage_channels != True:
                    await message.channel.send(">>> **このコマンドはヘルパー以上の役職を持っていないと使うことはできません**")
                    return
                new_crecord, changed, invalid_option = cmodify.modify_creator_record(msg[len('r!cmodify '):], cstr)
                if invalid_option:
                    await message.channel.send(">>> オプションが無効です。(使用可能オプション: 'LNAME' 'CNAME', 'CICON', 'ID', 'LINK')")
                elif not changed:
                    await message.channel.send(">>> 該当のレベルは存在しません")
                else:
                    with open(CPATH, "w") as record_file:
                        record_file.write(new_crecord)
                    await crecord_data.send(file=discord.File(CPATH))
                    await message.channel.send(">>> レコードを更新しました")
                    cstr = new_crecord
            
            # 'update': demonlistを取得してアップデート
            case 'update':
                if permi.manage_channels != True:
                    await message.channel.send(">>> **このコマンドはヘルパー以上の役職を持っていないと使うことはできません**")
                    return
                demonlist_data = client.get_channel(DEMONLIST)
                did = demonlist_data.last_message_id
                pid = precord_data.last_message_id

                demonlist = await demonlist_data.fetch_message(did)
                precord = await precord_data.fetch_message(pid)

                dbyte_data = await demonlist.attachments[0].read()
                pbyte_data = await precord.attachments[0].read()

                dstr = dbyte_data.decode()
                pstr = pbyte_data.decode()
                pstr = update.update_list(dstr, pstr)
                print(pstr)
                await message.channel.send(">>> Demonlistをアップデートしました")

            # 入力は有効なコマンドではない
            case _:
                await message.channel.send(">>> 有効なコマンドではありません")
                pass

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)