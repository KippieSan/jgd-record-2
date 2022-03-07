# JGD Recordの使い方

## **現在使えるコマンド一覧**
```
r!p
r!pcommit
r!pdelete
```

## **各コマンドの説明**

### `r!p`
レコードを表示します。

### `r!pcommit`
レコードを追加します。引数は次の通りです。
`r!pcommit level-name, player-icon [-1]`

demon listを上から走査し、レベル名が一致したものがあればその場所にレコードを追加します。同名のレベルが存在しないかつ`-1`が指定されていない場合その旨が報告されます。

`-1`が指定されているかつdemon list上に同名のレベルが存在しない場合、レベルは圏外組に追加されます。

例えば
```
r!pcommit Sonic Wave Infinity, :Spa:
r!pcommit kowareta, :Cob:
r!pcommit 1330X, :Blu: -1
```

などのように使います。既にレコード上にあるもの、ないものは自動で判定して追加します。

### `r!pdelete`
レコードを削除します。引数は次の通りです。
`r!pdelete level-name, [player-icon]`

`player-icon`はオプションです。
`player-icon`が指定されていない場合、レコードから同名レベルを見つけ、そのレコードを削除します。

`player-icon`が指定されている場合、同名レベルの中で、該当の`player-icon`のみを削除します。`player-icon`が削除されることで、該当のレベルからレコードが消える場合はレベルも消えます。

例えば
```
r!pdelete SonicWaVe
r!pdelete Slaughterhouse :Kip:
```

などのように使います。
