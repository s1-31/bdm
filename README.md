# bdm
big dream magnum

## raspberry pi
- hostname: s1-31

### ディスプレイでタッチが効かないときの対応
- 電源を切る
- SDカードを刺し直す
- ディスプレイをちょっとごにょごにょする
- 電源を入れ直す

### ssh のコマンドラインからディスプレイ表示系に干渉できないことへの対応
- ```export DISPLAY=:0```と入力する

### Accessoriesにアプリを追加する方法
- ```/usr/share/applications/```にアクセスする
- <アプリ名>.desktop　という形式でファイルを作成する

### デスクトップツールバー上のアイコンの配置や大きさをいじる
- ~/.config/lxpanel/LXDE-pi/panels/panel
- 参考サイト: http://ozzmaker.com/2014/06/30/virtual-keyboard-for-the-raspberry-pi/#more-2221(キーボードを出す)
- 参考サイト2: http://wiki.lxde.org/en/LXPanel
- アプリを配置したいなら、```type = launchbar```のところにdesktopファイルを追記すればよい

###一つのボタンでアプリのon/offを管理する
- ```/usr/bin/toggle-*.sh```を参考にすると良い。そしてそれを対象のdesktopファイルの```EXEC```にセットすれば完了。

###動画再生
- ```export DISPLAY=:0```を実行した上で、```mplayer -zoom -x 300 -y 200 -geometry 50%:50%```とやれば画面にちょうど収まる。
