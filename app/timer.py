# -*- coding:UTF-8 -*-

# Dependencies
#   please install curl, for example
#   (Ubuntu)
#   $ sudo apt-get insatll python-pygame

# PyGTKモジュールのインポート
import pygtk
pygtk.require('2.0')
import gtk, gobject

import datetime
import locale
import threading
import time
import os

import voice
import weather
import PiGPIO

import pygame

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

# 目覚まし
class Timer:
    def __init__(self):
        # 描画の初期化
        self.init_Window()

        # 機能の初期化
        self.init_Function()

    # 描画の初期化
    def init_Window(self):
        #ウィンドウを作成
        self.window = gtk.Window()
        self.window.set_border_width(5)
        self.window.set_size_request(300, 200)
        self.window.set_title('BDM')
        self.window.connect('destroy_event', self.end_application)
        self.window.connect('delete_event', self.end_application)
        # ラベルを作成
        self.label_show = gtk.Label()
        self.label_str = '<big><b>Hi!</b></big>'
        self.button_quit = gtk.Button()
        self.button_quit.set_label('Quit')
        self.button_quit.connect('clicked', self.end_application)
        # 現在時刻取得ボタン
        self.button_now = gtk.Button()
        self.button_now.set_label('What time is it now ?')
        self.button_now.connect('clicked', self.set_nowTime_txt)
        # テキストボックス作成
        # self.entry = gtk.Entry()
        #set timerボタン
        self.button_timerSet = gtk.Button('Set Timer')
        self.button_timerSet.connect('clicked', self.timerSet_clicked)
        # スピンボタン
        # 時間(Hour)
        self.adjHour = gtk.Adjustment(value=8, lower=0, upper=23, step_incr=1, page_incr=1)
        self.spHour = gtk.SpinButton(adjustment=self.adjHour, digits=1)
        self.spHour.set_wrap(True)
        # 分
        self.adjMinute = gtk.Adjustment(value=0, lower=0, upper=59, step_incr=1, page_incr=10)
        self.spMinute = gtk.SpinButton(adjustment=self.adjMinute, digits=1)
        self.spMinute.set_wrap(True)
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
    def init_Function(self):
        # タイマーを保持する配列
        self.timers = []

        # アラーム機能の初期化
        self.alarm_enable = True
        gobject.threads_init()
        gtk.gdk.threads_init()
        gtk.gdk.threads_enter()
        self.alarm_thread = threading.Thread(target=self.alarm, name="alarm", args=())
        self.alarm_thread.start()
        gtk.gdk.threads_leave()

        self.gpio = PiGPIO()


    # アプリが終了するときに呼ばれる関数
    def end_application(self, widget, data=None):
        self.alarm_enable = False
        self.alarm_thread.join()
        gtk.main_quit()
        return False

    # 現在時刻取得ボタンが押された時に呼ばれるボタン
    def set_nowTime_txt(self, widget, data=None):
        # ラベルに文字列を設定
        d = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.label_show.set_markup("<big><b>" + d + "</b></big>")

    # タイマーセットボタンが押された時に呼ばれる関数
    def timerSet_clicked(self, widget, data=None):
        hour = self.spHour.get_value_as_int()
        minute = self.spMinute.get_value_as_int()
        timer = self.setTimers(hour, minute, True)
        # if timer == False :
            # print "No More Timer..."
            # return
        self.check.set_label(str(hour)+"時"+str(minute)+"分")
        print "new timer : ", timer
        return

    # 一つ目のチェックボックスがオン・オフされた時に呼ばれる関数
    def on_toggle_check_1(self, widget=None, data=None):
        if widget.get_active():
            print 'check 1 is ON'
            self.timers[0]['enable'] = True
            print self.timers[0]
        else:
            print 'check 1 is OFF'
            self.timers[0]['enable'] = False
            print self.timers[0]

    # 配列timersに新しくtimerを追加する（排他処理）
    @synchronized(lock)
    def setTimers(self, hour, minute, enable):
        if (len(self.timers) > 0): # とりあえずタイマーは１個までしか登録できない仕様にしている
            # return False
            self.timers = []

        timer = {
            "hour" : hour,
            "minute" : minute,
            "enable" : enable,
            "check_box" : len(self.timers)
        }
        self.timers.append(timer)
        self.check.set_active(True)
        return timer

    # 配列timersから各timerを取得する（排他処理）
    @synchronized(lock)
    def getTimers(self, all):
        enable_timers = []
        for timer in self.timers:
            if( timer['enable'] or all):
                enable_timers.append(timer)
        return enable_timers

    # アラーム機能
    def alarm(self):

        pygame.mixer.init()
        pygame.mixer.music.load('../wav/nyan-cat.mp3')

        while self.alarm_enable:
            # 現在時刻取得
            now = datetime.datetime.now()
            print "now : ", now.hour, now.minute, now.second

            # タイマーと現在時刻が一致するものがないか
            timers = self.getTimers(False)
            for timer in timers:
                if ( now.hour == timer['hour'] and now.minute == timer['minute']):
                    self.notification(now) # アラーム時刻になった時の動作
                    print 'wait...'
                    print_time = time.time() # 導通待ちの間のprint間隔を保持するための時間
                    while not self.gpio.check_conduction():
                        if time.time() - print_time > 3: # 3秒に１回printする
                            print 'wait...'
                            print_time = time.time()
                        pass
                    self.finish_func(now)
                    self.check.set_active(False) # アラームが鳴ったらチェックボックスをDisnableする
                    timer['enable'] = False # アラームが鳴ったらそのタイマーはDisnableする
            time.sleep(1) # 現在時刻を取得する周期
        return

    # アラーム時刻になった時の動作
    def notification(self, now):

    	self.gpio.conduction_power_on()

        pygame.mixer.music.play(-1) # ()内は再生回数 -1:ループ再生

        print "#########################"
        print "######### ALARM #########"
        print "#########################"
        print "#########",now.hour, now.minute,"#########"
        print "#########################"

        print 'motor on'
        self.gpio.motor_power_on()
        time.sleep(5)
        self.gpio.motor_power_off()
        print 'motor off'

        print 'get weather'
        text = weather.Weather().get_string()
        print 'get voice'
        voice.VoiceText().getVoice(text=text)

    # アラームが止められた後の処理
    def finish_func(self, now):

        print 'stop music'
        pygame.mixer.music.pause() # 音楽の一時停止
        pygame.mixer.music.stop() # 再生の終了

        print "play voice..."

        voice.VoiceText().playVoice()

        self.gpio.conduction_power_off()
        self.gpio.cleanup()

        print "finish..."

if __name__=='__main__':
    print "hello" # 目覚ましアプリスタート

    timer = Timer()
    gtk.main()

    print "good bye" # 目覚ましアプリ終了
