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
# import PiGPIO

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
        self.window.set_title('目覚マシマシ')
        self.window.connect('destroy_event', self.end_application)
        self.window.connect('delete_event', self.end_application)
        # ラベルを作成
        self.label_show = gtk.Label()
        self.label_str = '<big><b>Hi!</b></big>'
        self.button_quit = gtk.Button()
        self.button_quit.set_label('Quit')
        self.button_quit.connect('clicked', self.end_application)
        # 現在時刻取得ボタン
        # self.button_now = gtk.Button()
        # self.button_now.set_label('What time is it now ?')
        # self.button_now.connect('clicked', self.set_nowTime_txt)
        # テキストボックス作成
        # self.entry = gtk.Entry()
        #set timerボタン
        self.button_timerSet = gtk.Button('Set Timer')
        self.button_timerSet.connect('clicked', self.timerSet_clicked)
        # スピンボタン
        # 時間(Hour)
        self.entry_hour = gtk.Entry()
        self.entry_hour.set_text('0')
        self.entry_hour.set_size_request(40,40)
        self.hour_button_up = gtk.Button("△")
        self.hour_button_up.set_size_request(50,40)
        self.hour_button_up.connect('clicked', self.hour_up)
        self.hour_button_down = gtk.Button('▽')
        self.hour_button_down.set_size_request(50,40)
        self.hour_button_down.connect('clicked', self.hour_down)
        self.hour_buttons = gtk.VBox()
        self.hour_buttons.add(self.hour_button_up)
        self.hour_buttons.add(self.hour_button_down)
        self.hour = gtk.HBox()
        self.hour.add(self.entry_hour)
        self.hour.add(self.hour_buttons)
        # 分
        self.entry_minute = gtk.Entry()
        self.entry_minute.set_text('0')
        self.entry_minute.set_size_request(40,40)
        self.minute_button_up = gtk.Button('△')
        self.minute_button_up.set_size_request(50,40)
        self.minute_button_up.connect('clicked', self.minute_up)
        self.minute_button_down = gtk.Button('▽')
        self.minute_button_down.set_size_request(50,40)
        self.minute_button_down.connect('clicked', self.minute_down)
        self.minute_buttons = gtk.VBox()
        self.minute_buttons.add(self.minute_button_up)
        self.minute_buttons.add(self.minute_button_down)
        self.minute = gtk.HBox()
        self.minute.add(self.entry_minute)
        self.minute.add(self.minute_buttons)

        self.spins = gtk.HBox()
        self.spins.add(self.hour)
        self.spins.add(self.minute)
        # セットされたタイマーのチェックボックス
        self.timersVbox = gtk.VBox()
        self.check1 = gtk.CheckButton('empty')
        self.check2 = gtk.CheckButton('empty')
        self.check1.connect('toggled', self.on_toggle_check_1)
        self.check2.connect('toggled', self.on_toggle_check_2)
        self.timersVbox.pack_start(self.check1)
        self.timersVbox.pack_start(self.check2)
        # セットされたタイマーのチェックボックスを格納したフレーム
        self.checkFrm = gtk.Frame('Timers')
        self.checkFrm.add(self.timersVbox)
        # ラベルとボタンをVBoxにパック
        self.vbox = gtk.VBox()
        self.vbox.add(self.label_show)
        self.vbox.add(self.spins)
        # self.vbox.add (self.button_now)
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

        # self.gpio = PiGPIO()

    # アプリが終了するときに呼ばれる関数
    def end_application(self, widget, data=None):
        self.alarm_enable = False
        self.alarm_thread.join()
        gtk.main_quit()
        return False

    # タイマーセットボタンが押された時に呼ばれる関数
    def timerSet_clicked(self, widget, data=None):
        hour = int(self.entry_hour.get_text())
        minute = int(self.entry_minute.get_text())
        timer = self.setTimers(hour, minute, True)
        # if timer == False :
            # print "No More Timer..."
            # return
        if timer['check_box'] == 1:
            self.check1.set_label(str(hour)+"時"+str(minute)+"分")
        else:
            self.check2.set_label(str(hour)+"時"+str(minute)+"分")

        print "new timer : ", timer
        return

    # 一つ目のチェックボックスがオン・オフされた時に呼ばれる関数
    def on_toggle_check_1(self, widget=None, data=None):
        print 'toggle'
        timers = self.getTimers(all=True)
        this_timer = None
        print 'timer in timers'
        for timer in timers:
            if timer['check_box'] == 1:
                this_timer = timer
        if not this_timer:
            return

        if widget.get_active():
            print 'check 1 is ON'
            this_timer['enable'] = True
        else:
            print 'check 1 is OFF'
            this_timer['enable'] = False

    # 2つ目のチェックボックスがオン・オフされた時に呼ばれる関数
    def on_toggle_check_2(self, widget=None, data=None):
        print 'toggle'
        timers = self.getTimers(all=True)
        this_timer = None
        print 'timer in timers'
        for timer in timers:
            if timer['check_box'] == 2:
                this_timer = timer
        if not this_timer:
            return

        if widget.get_active():
            print 'check 2 is ON'
            this_timer['enable'] = True
        else:
            print 'check 2 is OFF'
            this_timer['enable'] = False

    # 配列timersに新しくtimerを追加する（排他処理）
    # @synchronized(lock)
    def setTimers(self, hour, minute, enable):
        change_timer = None
        num1_timer = None
        for timer in self.timers:
            if timer['enable'] == False:
                change_timer = timer
            if timer['check_box'] == 1:
                num1_timer = timer
                if num1_timer == change_timer:
                    break

        if change_timer == None and len(self.timers) == 2:
            self.timers.remove(num1_timer)
            num = 1
        elif len(self.timers) == 2:
            num = change_timer['check_box']
            self.timers.remove(change_timer)
        else: # とりあえずタイマーは１個までしか登録できない仕様にしている
            if num1_timer == None:
                num = 1
            else:
                num = 2

        timer = {
            "hour" : hour,
            "minute" : minute,
            "enable" : enable,
            "check_box" : num
        }
        self.timers.append(timer)
        if num == 1:
            self.check1.set_active(True)
        if num == 2:
            self.check2.set_active(True)

        return timer

    # 配列timersから各timerを取得する（排他処理）
    # @synchronized(lock)
    def getTimers(self, all=False):
        enable_timers = []
        for timer in self.timers:
            if timer['enable'] or all:
                enable_timers.append(timer)
        return enable_timers

    # アラーム機能
    def alarm(self):

        pygame.mixer.init()
        pygame.mixer.music.load('../wav/nyan-cat.mp3')

        while self.alarm_enable:
            # 現在時刻取得
            now = datetime.datetime.now()
            # print "now : ", now.hour, now.minute, now.second
            d = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            self.label_show.set_markup("<big><b>" + d + "</b></big>")

            # タイマーと現在時刻が一致するものがないか
            timers = self.getTimers(False)
            for timer in timers:
                if ( now.hour == timer['hour'] and now.minute == timer['minute']):
                    self.notification(now) # アラーム時刻になった時の動作
                    print 'wait...'
                    print_time = time.time() # 導通待ちの間のprint間隔を保持するための時間
                    # while not self.gpio.check_conduction():
                    while True:
                        if time.time() - print_time > 3: # 3秒に１回printする
                            print 'wait...'
                            print_time = time.time()
                        time.sleep(2)
                        break
                        pass
                    self.finish_func(now)
                    if timer['check_box'] == 1:
                        self.check1.set_active(False) # アラームが鳴ったらチェックボックスをDisnableする
                    else:
                        self.check2.set_active(False) # アラームが鳴ったらチェックボックスをDisnableする

                    timer['enable'] = False # アラームが鳴ったらそのタイマーはDisnableする
            time.sleep(1) # 現在時刻を取得する周期
        return

    # アラーム時刻になった時の動作
    def notification(self, now):

    	# self.gpio.conduction_power_on()

        pygame.mixer.music.play(-1) # ()内は再生回数 -1:ループ再生

        print "#########################"
        print "######### ALARM #########"
        print "#########################"
        print "#########",now.hour, now.minute,"#########"
        print "#########################"

        print 'motor on'
        # self.gpio.motor_power_on()
        # time.sleep(5)
        # self.gpio.motor_power_off()
        print 'motor off'

        print 'get weather'
        text = weather.Weather().get_string()
        print 'get voice'
        voice.VoiceText().getVoice(text=text,speaker='haruka',emotion='happiness',level=4)

    # アラームが止められた後の処理
    def finish_func(self, now):

        print 'stop music'
        time.sleep(1)

        pygame.mixer.music.pause() # 音楽の一時停止
        pygame.mixer.music.stop() # 再生の終了

        print "play voice..."
        time.sleep(1)

        voice.VoiceText().playVoice()

        # self.gpio.conduction_power_off()
        # self.gpio.cleanup()

        print "finish..."

    def hour_up(self, widget=None, data=None):
        print 'hour up'
        hour = int(self.entry_hour.get_text())
        hour = (hour+1) % 24
        self.entry_hour.set_text(str(hour))

    def hour_down(self, widget=None, data=None):
        print 'hour down'
        hour = int(self.entry_hour.get_text())
        hour = (hour-1) % 24
        self.entry_hour.set_text(str(hour))

    def minute_up(self, widget=None, data=None):
        print 'minute up'
        minute = int(self.entry_minute.get_text())
        minute = (minute+1) % 60
        self.entry_minute.set_text(str(minute))

    def minute_down(self, widget=None, data=None):
        print 'minute down'
        minute = int(self.entry_minute.get_text())
        minute = (minute-1) % 60
        self.entry_minute.set_text(str(minute))


if __name__=='__main__':
    print "hello" # 目覚ましアプリスタート

    timer = Timer()
    gtk.main()

    print "good bye" # 目覚ましアプリ終了
