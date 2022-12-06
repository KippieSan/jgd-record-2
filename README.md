# JGD Record
[Japan Geometry Dash](https://discord.gg/G3ACWnU)のPlayer-Records及びCreator-Recordsを管理するbotです。
定数以外のコードはここで公開しているのでバグ等を見つけた場合は上のサーバーの`#suggestion`や`#general`、もしくは`Issues`などで報告していただけると幸いです。

# JGD Recordの使い方

**2022/11/22にスラッシュコマンドへの対応を行ったため, 各コマンドの詳細がコマンド選択時, 引数の説明が引数の入力時に表示されるようになりました.**

## **現在使えるコマンド一覧**
```
/p
/pcommit
r/plcommit
/pdelete

/update

/c
/ccommit
/cdelete
/cmodify
```

## **各コマンドの説明**

### `/p`
プレイヤーレコードを表示します。

### `/pcommit`
レコードを追加します。引数は次の通りです。
```
/pcommit level-name, player-icon, is_listed
```

demon listを上から走査し、レベル名が一致したものがあればその場所にレコードを追加します。同名のレベルが存在しないかつ`is_listed=True`である場合その旨が報告されます。
`is_listed=False`が指定されているかつdemon list上に同名のレベルが存在しない場合、レベルは圏外組に追加されます。
`is_listed`はデフォルトでは`True`に設定されています

例えば
```
/pcommit Sonic Wave Infinity, :Spa:
/pcommit kowareta, :Cob:
/pcommit 1330X, :Blu:, False
```

などのように使います。既にレコード上にあるもの、ないものは自動で判定して追加します。

### `/plcommit`
レコードをリスト形式で追加します。引数は次の通りです。
```
/plcommit level1, level2, level3,..., leveln, player-icon
```

`/pcommit`を各レベルで呼び出し、levelに既に追加されているレベルがあれば、そのレベルのリストを、
存在しないレベルがあれば、そのレベルのリストを出力します。
`is_listed`オプションはリスト内にあるレベルの名称を間違えていた場合`Blood BAth`が圏外にあるといったことが起こるので現在は
サポートされていません。

カンマ直後に1マスのスペースがある場合はトリミングされます。

例えば
```
/plcommit Sonic Wave, Sonic Wave Infinity, Generic Wave,Sonic Wave Rebirth, :Spa:
```
などのように使います。

### `/pdelete`
レコードを削除します。引数は次の通りです。
```
/pdelete level-name, [player-icon]
```

`player-icon`はオプションです。
`player-icon`が指定されていない場合、レコードから同名レベルを見つけ、そのレコードを削除します。

`player-icon`が指定されている場合、同名レベルの中で、該当の`player-icon`のみを削除します。`player-icon`が削除されることで、該当のレベルからレコードが消える場合はレベルも消えます。

例えば
```
/pdelete SonicWaVe
/pdelete Slaughterhouse :Kip:
```

などのように使います。

### `/update`
Demonlistがアップデートされた際に使います。
Demonlistを[pointercrate](https://pointercrate.com/demonlist/)より取得し, DemonlistおよびPlayer Recordsのアップデートを行います
```
/update
```


### `/c`
クリエイターレコードを表示します

### `/ccommit`
レコードを追加します。引数は次の通りです。
```
r!ccommit level-name, creator-name, creator-icon, level-id, [video-link], [insert_after]
```

`video-link`はレベルのプレイ動画がある場合に指定することで、レコードに動画へのリンクが貼られます。
`insert_after`はレベルをリストの途中に追加したいときにここにレベルを指定することで, このレベルの直後にレコードを追加します.

例えば
```
/ccommit Level 21, Spaces, :Spa:, 11221122
/ccommit Rated Level, Spaces, :Spa:, 22112211, link = youtube.link
/ccommit Test Level, Kippie, :Kip:, 11111111, insert_after = GAME TIME
/ccommit Test Level2, Kippie, :Kip:, 111111222, link = youtube.link, insert_after = Optimism
```
などのように使います。

### `/cdelete`
レコードを削除します。引数は次の通りです。
```
/cdelete level-name
```

該当レベルと同名のレベルをレコードから削除します。レコードにレベルが存在しない場合は何もしません。
例えば
```
/cdelete GameTIMe
```
などのように使います。

### `/cmodify`
レコードの情報を編集します。引数は次の通りです。
```
/cmodify level-name, option, modified
```

`option`には以下の五つを指定できます
```
LNAME - レベル名
CNAME - クリエイターの名前
CICON - クリエイターのアイコン
ID    - レベルID
LINK  - 動画へのリンク
```

`option`で指定されたフィールドを`modified`に書き換えます。

例えば
```
/cmodify FFOOFF, LNAME, FF00FF
```
などのように使います。
