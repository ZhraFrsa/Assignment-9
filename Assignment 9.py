import telebot
from telebot import types
import random
import qrcode
import datetime
import gtts



bot = telebot.TeleBot("5023759011:AAGmhACMWBuuTdmUOFAorReWJllxXxYcVlw")


#______________________________________________________________________________________________#


@bot.message_handler(commands=['help'])
def help_func(message):
    btn=["/game","/age","/voice","/max","/indexmax","/qrcode"]

    markup = telebot.types.ReplyKeyboardMarkup(row_width=len(btn))
    for i in btn:

        bottun = telebot.types.KeyboardButton(i)
    
        markup.add(bottun)
    bot.send_message(message.chat.id, 'menu:',reply_markup=markup)


#______________________________________________________________________________________________#


@bot.message_handler(commands=['start'])
def start_func(message):

    btn=["/game","/age","/voice","/max","/indexmax","/qrcode"]

    markup = telebot.types.ReplyKeyboardMarkup(row_width=len(btn))
    for i in btn:

        bottun = telebot.types.KeyboardButton(i)
    
        markup.add(bottun)
    bot.send_message(message.chat.id, 'خوش آمدی ' + (message.chat.first_name),reply_markup=markup)
#______________________________________________________________________________________________#


@bot.message_handler(commands=['game'])
def guse_number_game(message):
    
    mm = bot.send_message(message.chat.id, 'عدد بین اعداد 0 تا 100 است موفق باشید ')
    global number
    number = random.randint(0, 99)
    bot.register_next_step_handler(mm, game_play)

def game_play(mm):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    bottun = telebot.types.KeyboardButton('New Game')
    
    markup.add(bottun)
   
    
    if mm.text == "New Game":
        mm = bot.send_message(mm.chat.id,'بازی جدید شروع شد ',reply_markup=markup)
                                     
        
        
        bot.register_next_step_handler(mm, guse_number_game)
    else:
        try:
            if int(mm.text) < number:
                mm = bot.send_message(mm.chat.id, 'برو بالا', reply_markup=markup)
                bot.register_next_step_handler(mm, game_play)
            elif int(mm.text) > number:
                mm = bot.send_message(mm.chat.id, 'برو پایین', reply_markup=markup)
                bot.register_next_step_handler(mm, game_play)
            else:
                markup = telebot.types.ReplyKeyboardRemove(selective=True)
                bot.send_message(mm.chat.id, '🥳', reply_markup=markup)
                bot.send_message(mm.chat.id, 'برنده شدی', reply_markup=markup)
        except:
            mm = bot.send_message(mm.chat.id, '!عدد وارد کنید ' , reply_markup=markup)
            bot.register_next_step_handler(mm, game_play)
        
#______________________________________________________________________________________________#


@bot.message_handler(commands=['age'])
def age_func(m):
    message = bot.send_message(m.chat.id, 'تاریخ تولدتان را مانند مثال روبرو ارسال کنید (1400/9/18)')
    bot.register_next_step_handler(message, age_play)

def age_play(message):
    x = datetime.datetime.now()
    global gy
    gy=x.year
    global gm
    gm=x.month
    global gd
    gd=x.day
    yy,mm,dd = message.text.split("/")   
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if (gm > 2):
        gy2 = gy + 1
    else:
        gy2 = gy
    days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
    jy = -1595 + (33 * (days // 12053))
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if (days > 365):
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if (days < 186):
        jm = 1 + (days // 31)
        jd = 1 + (days % 31)
    else:
        jm = 7 + ((days - 186) // 30)
        jd = 1 + ((days - 186) % 30)    
    yy=int(yy)
    mm=int(mm) 
    dd=int(dd)    
    if(jd < dd):
        jm-=1
        jd+=30            
    if(jm < mm):
        jm += 12
        jy -= 1     
    yy = jy - yy
    mm = jm - mm
    dd = jd - dd
    if yy>=1:
        h=yy*362*24
        min=h*60
        sec=min*60
    else :
        if mm>=1:
            h=mm*7*24
            min=h*60
            sec=min*60
        else:
            h=dd*24
            min=h*60
            sec=min*60 

    bot.send_message(message.chat.id, "شما  " +str(yy) +" سال  "+ str(mm) +" ماه و "+ str(dd)+" روز دارید " )
    
#______________________________________________________________________________________________#

@bot.message_handler(commands=['voice'])
def voice_func(message):
    message = bot.send_message(message.chat.id, 'نوشته انگلیسی را وارد نمایید')
    bot.register_next_step_handler(message, voice_play)


def voice_play(message):
    if not message.text.startswith('/'):
        try:
            vc = gtts.gTTS(text=message.text)
            vc.save('voice.ogg')
            voice = open('voice.ogg','rb')
            bot.send_voice(message.chat.id, voice)
        except:
            bot.send_message(message.chat.id, 'کلمات با معنی انگیلسی وارد نمایید')
    else:
        bot.reply_to(message, '!کامند وارد کردین')
        
#______________________________________________________________________________________________#


@bot.message_handler(commands=['max'])
def max_func(message):
    message = bot.send_message(message.chat.id, 'اعداد خود را مثل مثال وارد کنید 2,3,1,4,5')
    bot.register_next_step_handler(message, max_play)


def max_play(message):
        try:
            numbers = list(map(int, message.text.split(',')))
            bot.send_message(message.chat.id, 'بزرگترین : ' + str(max(numbers))+" است ")
        except:
            bot.send_message(message.chat.id, 'مثل مثال وارد کنید')

#______________________________________________________________________________________________#
       

@bot.message_handler(commands=['indexmax'])
def indexmax_welcome(message):
    message = bot.send_message(message.chat.id, 'اعداد خود را مثل مثال وارد کنید 2,3,1,4,5')
    bot.register_next_step_handler(message, indexmax)


def indexmax(message):
    if not message.text.startswith('/'):
        try:
            numbers = list(map(int, message.text.split(',')))
            bot.send_message(message.chat.id, 'اندیس بزرگترین عدد: ' + str(numbers.index(max(numbers))))
        except:
            bot.send_message(message.chat.id, 'مثل مثال وارد کنید')

#______________________________________________________________________________________________#
 

@bot.message_handler(commands=['qrcode'])
def Qrcode(message):
    message = bot.send_message(message.chat.id, 'نوشته خود را بنویسید' )
    bot.register_next_step_handler(message, qr)


def qr(message):
    if not message.text.startswith('/'):
            img = qrcode.make(message.text)
            img.save('QRcode.png')
            photo = open('QRcode.png', 'rb')
            bot.send_photo(message.chat.id, photo)
        


bot.infinity_polling()