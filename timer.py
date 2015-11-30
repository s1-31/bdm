# -*- coding:UTF-8 -*-

# PyGTKモジュールのインポート
import pygtk
pygtk.require('2.0')
import gtk

import datetime
import locale

class Timer:
    def __init__(self):
        #ウィンドウを作成
        self.window = gtk.Window()
        self.window.set_border_width(5)
        self.window.set_size_request(400, 300)
        self.window.set_title('BDM')
        self.window.connect('destroy_event', self.end_application)
        self.window.connect('delete_event', self.end_application)

        #ボタンが押されるごとに表示が変わるラベルを作成
        self.label_show = gtk.Label()
        self.label_show.set_markup('<big><b>Hi!</b></big>')

        self.button_now = gtk.Button()
        self.button_now.set_label('What time is it now ?')
        self.button_now.connect('clicked', self.set_nowTime_txt)

        #押すとアプリケーションを終了するボタンを作成
        self.button_quit = gtk.Button()
        self.button_quit.set_label('Quit')
        self.button_quit.connect('clicked', self.end_application)

        # テキストボックス作成
        # self.entry = gtk.Entry()

        #Setボタン
        self.button_timerSet = gtk.Button('Set Timer')
        self.button_timerSet.connect('clicked', self.timerSet_clicked)

        self.adjHour = gtk.Adjustment(value=8, lower=0, upper=23, step_incr=1, page_incr=1)
        self.adjMinute = gtk.Adjustment(value=0, lower=0, upper=59, step_incr=1, page_incr=10)
        self.spHour = gtk.SpinButton(adjustment=self.adjHour, digits=1)
        self.spMinute = gtk.SpinButton(adjustment=self.adjMinute, digits=1)

        self.spins = gtk.HBox()
        self.spins.add(self.spHour)
        self.spins.add(self.spMinute)

        self.timersVbox = gtk.VBox()
        self.check = gtk.CheckButton('empty')
        self.check.connect('toggled', self.on_toggle_check_1)
        self.timersVbox.pack_start(self.check)

        self.checkFrm = gtk.Frame('Timers')
        self.checkFrm.add(self.timersVbox)

        # ラベルとボタンをVBoxにパック
        self.vbox = gtk.VBox()
        self.vbox.add(self.label_show)
        self.vbox.add(self.spins)
        # self.vbox.add(self.entry)
        self.vbox.add(self.button_now)
        self.vbox.add(self.button_timerSet)
        self.vbox.add(self.button_quit)

        self.hbox = gtk.HBox()
        self.hbox.pack_start(self.vbox)
        self.hbox.pack_start(self.checkFrm)

        # VBoxをウィンドウに格納
        self.window.add(self.hbox)

        # ウィンドウ、および配下の全ウィジェットを表示
        self.window.show_all()

    # def messagebox(self, text):
    #     dialog = gtk.MessageDialog(
    #         self.window,
    #         gtk.DIALOG_MODAL,
    #         gtk.MESSAGE_INFO,
    #         gtk.BUTTONS_OK,
    #         text,
    #     )
    #     dialog.run()
    #     dialog.destroy()

    def end_application(self, widget, data=None):
        gtk.main_quit()
        return False

    def set_nowTime_txt(self, widget, data=None):
        # ラベルに文字列を設定
        d = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.label_show.set_markup("<big><b>" + d + "</b></big>")

    def timerSet_clicked(self, widget, data=None):
        # self.messagebox(u'入力内容は%sです' % self.entry.get_text())
        print 'a'

    def on_toggle_check_1(self, widget=None, data=None):
        if widget.get_active():
            print 'check 1 is ON'
        else:
            print 'check 1 is OFF'

def main():
    hw = Timer()
    gtk.main()

if __name__=='__main__':
    main()
