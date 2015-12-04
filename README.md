# bdm
big dream magnum

## raspberry pi
- hostname: s1-31

### ディスプレイでタッチが効かないときの対応
- 電源を切る
- SDカードを刺し直す
- ディスプレイをちょっとごにょごにょする
- 電源を入れ直す
- 

### ssh のコマンドラインからディスプレイ表示系に干渉できないことへの対応
- ```export DISPLAY=:0```と入力する

### Accessoriesにアプリを追加する方法
- ```/usr/share/applications/```にアクセスする
- <アプリ名>.desktop　という形式でファイルを作成する

### デスクトップのアイコンの配置や大きさをいじれる?
- ~/.config/lxpanel-pi/LXDE/panels/panel
- 参考サイト：http://ozzmaker.com/2014/06/30/virtual-keyboard-for-the-raspberry-pi/#more-2221(キーボードを出す)
