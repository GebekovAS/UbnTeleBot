#!/usr/bin/python
# -*- coding: utf-8 -*-
import telebot
import os
from subprocess import Popen, PIPE

def accessTest (message):
        result=False
        try :
                f = open('/home/user/ac_list.txt','a+')
                isRec=True
                for line in f:
                        ln_arr=line.split(':')
                        if len(ln_arr)>2:
                                if ln_arr[1]==str(message.chat.id) and  ln_arr[0]==message.chat.username:
                                        isRec=False
                                        result=ln_arr[2]=='ok'
                if isRec:
                        f.write(message.chat.username+':'+str(message.chat.id)+':no:\n')
                f.close()
        except:
                result=False
        return result


while True:
        try:
                bot = telebot.TeleBot("token")

                @bot.message_handler(commands=['help', 'start'])
                def send_welcome(message):
                        if accessTest(message):
                                bot.send_message(message.chat.id, 'Ожидаю команды')
                        else :
                                bot.send_message(message.chat.id, 'Ожидайте авторизации')

                @bot.message_handler(commands=['reboot'])
                def reboot_func(message):
                        if accessTest(message):
                                bot.send_message(message.chat.id, 'Выполняю перезагрузку')
                                os.system("reboot")
                        else :
                                bot.send_message(message.chat.id, 'Ожидайте авторизации')

                @bot.message_handler(commands=['status'])
                def reboot_func(message):
                        if accessTest(message):
                                out, err = Popen('sh -c "virsh list"', shell=True, stdout=PIPE).communicate()
                                bot.send_message(message.chat.id, out)
                        else :
                                bot.send_message(message.chat.id, 'Ожидайте авторизации')

                @bot.message_handler(commands=['vm_restart'])
                def vm_restart_func(message):
                        if accessTest(message):
                                vname=message.text.split(' ')[1]
                                out, err = Popen('sh -c "virsh destroy '+vname+'"', shell=True, stdout=PIPE).communicate()
                                bot.send_message(message.chat.id, out)
                                out, err = Popen('sh -c "virsh start '+vname+'"', shell=True, stdout=PIPE).communicate()
								bot.send_message(message.chat.id, out)
                        else :
                                bot.send_message(message.chat.id, 'Ожидайте авторизации')

                @bot.message_handler(commands=['auth'])
                def send_auth(message):
                        pass

                bot.polling()
        except:
                pass






