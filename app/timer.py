# -*- coding:UTF-8 -*-

# PyGTKモジュールのインポート
import pygtk
pygtk.require('2.0')
import gtk, gobject

import datetime
import locale
import threading
import time

# 排他処理用のデコレータ
lock = threading.Lock()
def synchronized(lock):
    """ Synchronization decorator. """
    def wrap(f):
        def newFunction(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return newFunction
    return wrap

class Timer:
    def __init__(self):
        #ウィンドウを作成
        self.window = gtk.Window()
        self.window.set_border_width(5)
        self.window.set_size_request(300, 200)
        self.window.set_title('BDM')
        self.window.connect('destroy_event', self.end_application)
        self.window.connect('delete_event', self.end_application)

        # ラベルを作成
        self.label_str = '<big><b>Hi!</b></big>'
        self.button_quit.set_label('Quit')
        self.button_quit.connect('clicked', self.end_application)

        # テキストボックス作成
        # self.entry = gtk.Entry()

        #set timerボタン
        self.button_timerSet = gtk.Button('Set Timer')
        self.button_timerSet.connect('clicked', self.timerSet_clicked)

        # スピンボタン
        # 時間(Hour)
        self.adjHour = gtk.Adjustment(value=8, lower=0, upper=23, step_incr=1, page_incr=1)
        self.spHour = gtk.SpinButton(adjustment=self.adjHour, digits=1)
        # 分
        self.adjMinute = gtk.Adjustment(value=0, lower=0, upper=59, step_incr=1, page_incr=10)
        self.spMinute = gtk.SpinButton(adjustment=self.adjMinute, digits=1)

        self.spins = gtk.HBox()
        self.spins.add(self.spHour)
        self.spins.add(self.spMinute)

        # セットされたタイマーのチェックボックス
        self.timersVbox = gtk.VBox()
        self.check = gtk.CheckButton('empty')
        self.check.connect('toggled', self.on_toggle_check_1)
        self.timersVbox.pack_start(self.check)

        # セットされたタイマーのチェックボックスを格納したフレーム
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

        # チェックフレームとVBoxをHBoxに格納
        self.hbox = gtk.HBox()
        self.hbox.pack_start(self.vbox)
        self.hbox.pack_start(self.checkFrm)

        # HBoxをウィンドウに格納
        self.window.add(self.hbox)

        # ウィンドウ、および配下の全ウィジェットを表示
        self.window.show_all()

        # 機能の初期化
        self.timers = []

        # アラーム機能の初期化
        self.alarm_enable = True
        gobject.threads_init()
        gtk.gdk.threads_init()

        gtk.gdk.threads_enter()
        self.alarm_thread = threading.Thread(target=self.alarm, name="alarm", args=())
        self.alarm_thread.start()
        gtk.gdk.threads_leave()
        self.alarm_enable = False
        self.alarm_thread.join()
        return False

    def set_nowTime_txt(self, widget, data=None):
        # ラベルに文字列を設定
        d = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.label_show.set_markup("<big><b>" + d + "</b></big>")

    def timerSet_clicked(self, widget, data=None):
        hour = self.spHour.get_value_as_int()
        minute = self.spMinute.get_value_as_int()
        self.check.set_label(str(hour)+"時"+str(minute)+"分")

        timer = self.setTimers(hour, minute, True)
        print "new timer : ", timer

    def on_toggle_check_1(self, widget=None, data=None):
        if widget.get_active():
            print 'check 1 is ON'
            self.timers[0]['enable'] = True
            print self.timers[0]
        else:
            print 'check 1 is OFF'
            self.timers[0]['enable'] = False
            print self.timers[0]

    @synchronized(lock)
    def setTimers(self, hour, minute, enable):
        timer = {
            "hour" : hour,
            "minute" : minute,
            "enable" : enable,
            "check_box" : len(self.timers)
        }
        self.timers.append(timer)
        return timer

    @synchronized(lock)
    def getTimers(self, all):
        enable_timers = []
        for timer in self.timers:
            if( timer['enable'] or all):
                enable_timers.append(timer)
        return enable_timers

    def alarm(self):
        timers = self.getTimers(False)
        while self.alarm_enable:
            now = datetime.datetime.now()
            print now
            time.sleep(1)
            print self.getTimers(False)
            time.sleep(1)
        return


if __name__=='__main__':
    timer = Timer()
    print "hello"

    gtk.main()

    print "good bye"
