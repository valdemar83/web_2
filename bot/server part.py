import telebot
from telebot import types
from requests import get
from PIL import Image
from numpy import array
from math import sqrt

#@Fig_Calc_bot

bot = telebot.TeleBot('Token')
figure_chose_markup = telebot.types.ReplyKeyboardMarkup(True, True)
figure_chose_markup.row('Треугольник')
figure_chose_markup.row('Круг')
figure_chose_markup.row('Квадрат')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Привет, это бот для вычисления параметров геометрических фигур. Чтобы начать, выберите фигуру или свяжитесь с помощником (/admin):'
                     ,reply_markup = figure_chose_markup)
    
#   Написать помощнику 
@bot.message_handler(commands=['admin'])
def default_test(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Написать помощнику", url="https://t.me/Vladimir_dolar")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Эта кнопка поможет Вам связатся с помощником в решении Ваших задач:", reply_markup=keyboard)

            
@bot.message_handler(content_types=["text"])
def send_text(message):
    if message.text == 'Треугольник':
        bot.send_message(message.chat.id, 'Выбери круг',reply_markup = figure_chose_markup)
    elif message.text == 'Круг':
        circle_unknown_param(message)
    elif message.text == 'Квадрат':
        bot.send_message(message.chat.id, 'Выбери круг ',reply_markup = figure_chose_markup)
    else:
        bot.send_message(message.chat.id, 'Что-то пошло не так, начни со /start')
        
def circle_unknown_param(message):    
    circle_choose_unknown_param = telebot.types.ReplyKeyboardMarkup(True, True)
    circle_choose_unknown_param.row('r (найти радиус)', 'd (найти диаметр)' )
    circle_choose_unknown_param.row('l (найти длину круга)', 'S (найти площадь)')
    photo = Image.open('circle.png')
    bot.send_photo(message.chat.id, photo)
    #bot.send_message(message.chat.id, 'photo')
    bot.send_message(message.chat.id, 'Выбери неизвестный параметр: ',reply_markup = circle_choose_unknown_param)
    bot.register_next_step_handler(message, circle_choose_known_param)

def circle_choose_known_param(message):
    if message.text == 'r (найти радиус)':
        circle_choose_known_param = telebot.types.ReplyKeyboardMarkup(True, True)
        circle_choose_known_param.row('Длина, неизвестен радиус')
        circle_choose_known_param.row('Диаметр, неизвестен радиус')
        circle_choose_known_param.row('Площадь, неизвестен радиус')
        bot.send_message(message.chat.id, 'Выберите известный параметр:', reply_markup=circle_choose_known_param)
        bot.register_next_step_handler(message, circle_radius_by_smth)
    elif message.text == 'd (найти диаметр)':
        circle_choose_known_param = telebot.types.ReplyKeyboardMarkup(True, True)
        circle_choose_known_param.row('Радиус, неизвестен диаметр')
        circle_choose_known_param.row('Длина, неизвестен диаметр')
        circle_choose_known_param.row('Площадь, неизвестен диаметр')
        bot.send_message(message.chat.id, 'Выберите известный параметр:', reply_markup=circle_choose_known_param)
        bot.register_next_step_handler(message, circle_diametr_by_smth)
    elif message.text == 'l (найти длину круга)':
        circle_choose_known_param = telebot.types.ReplyKeyboardMarkup(True, True)
        circle_choose_known_param.row('Радиус, неизвестна длина')
        circle_choose_known_param.row('Диаметр, неизвестна длина')
        circle_choose_known_param.row('Площадь, неизвестна длина')
        bot.send_message(message.chat.id, 'Выберите известный параметр:', reply_markup=circle_choose_known_param)
        bot.register_next_step_handler(message, circle_length_by_smth)
    elif message.text == 'S (найти площадь)':
        circle_choose_known_param = telebot.types.ReplyKeyboardMarkup(True, True)
        circle_choose_known_param.row('Радиус, неизвестна площадь')
        circle_choose_known_param.row('Диаметр, неизвестна площадь')
        circle_choose_known_param.row('Длина, неизвестна площадь')
        bot.send_message(message.chat.id, 'Выберите известный параметр:', reply_markup=circle_choose_known_param)
        bot.register_next_step_handler(message, circle_square_by_smth)
        
    else:
        bot.send_message(message.chat.id, 'Что-то пошло не так, начни со /start')
        
def circle_radius_by_smth(message):
    one_time_keyboard = False
    if message.text == 'Длина, неизвестен радиус':
        bot.send_message(message.chat.id, 'Введите длину(см):')
        bot.register_next_step_handler(message, circle_radius_by_length)
    elif message.text == 'Диаметр, неизвестен радиус':
        bot.send_message(message.chat.id, 'Введите длину(см):')
        bot.register_next_step_handler(message, circle_radius_by_diametr)
    elif message.text == 'Площадь, неизвестен радиус':
        bot.send_message(message.chat.id, 'Введите площадь(см^2) *π:')
        bot.register_next_step_handler(message, circle_radius_by_square)
    else:
        bot.send_message(message.chat.id, 'Что-то пошло не так, начни со /start')
        
def circle_radius_by_length(message):
    length = int(message.text)/2
    length_text = str(length)
    answer = ['Ваш радиус:    ', length_text, '/π', ' (см)']
    answer = ''.join(answer)
    bot.send_message(message.chat.id, answer)

def circle_radius_by_diametr(message):
    diam = int(message.text)/2
    diam_text = str(diam)
    answer = ['Ваш радиус:    ', diam_text, ' (см)']
    answer = ''.join(answer)
    bot.send_message(message.chat.id, answer)
    
def circle_radius_by_square(message):
    square = sqrt(int(message.text))
    square_text = str(square)
    answer = ['Ваш радиус:    ', square_text, ' (см)']
    answer = ''.join(answer)
    bot.send_message(message.chat.id, answer)

def circle_diametr_by_smth(message):
    if message.text == 'Радиус, неизвестен диаметр':
        bot.send_message(message.chat.id, 'Введите радиус(см):')
        bot.register_next_step_handler(message, circle_diametr_by_radius)
    elif message.text == 'Длина, неизвестен диаметр':
        bot.send_message(message.chat.id, 'Введите длину(см):')
        bot.register_next_step_handler(message, circle_diametr_by_length)
    elif message.text == 'Площадь, неизвестен диаметр':
        bot.send_message(message.chat.id, 'Введите площадь(см^2) *π:')
        bot.register_next_step_handler(message, circle_diametr_by_square)
    else:
        bot.send_message(message.chat.id, 'Что-то пошло не так, начни со /start')

def circle_diametr_by_radius(message):
    radius = int(message.text)*2
    radius_text = str(length)
    answer = ['Ваш диаметр:    ', length_text, ' (см)']
    answer = ''.join(answer)
    bot.send_message(message.chat.id, answer)

def circle_diametr_by_length(message):
    length = int(message.text)
    length_text = str(length)
    answer = ['Ваш диаметр:    ', diam_text, '/π', ' (см)']
    answer = ''.join(answer)
    bot.send_message(message.chat.id, answer)
    
def circle_diametr_by_square(message):
    square = (sqrt(int(message.text)))*2
    square_text = str(square)
    answer = ['Ваш диаметр:    ', square_text, ' (см)']
    answer = ''.join(answer)
    bot.send_message(message.chat.id, answer)





def circle_length_by_smth(message):
    if message.text == 'Радиус, неизвестна длина':
        bot.send_message(message.chat.id, 'Введите радиус(см):')
        bot.register_next_step_handler(message, circle_length_by_radius)
    elif message.text == 'Диаметр, неизвестна длина':
        bot.send_message(message.chat.id, 'Введите диаметр(см):')
        bot.register_next_step_handler(message, circle_length_by_diametr)
    elif message.text == 'Площадь, неизвестна длина':
        bot.send_message(message.chat.id, 'Введите площадь(см^2) *π:')
        bot.register_next_step_handler(message, circle_length_by_square)
    else:
        bot.send_message(message.chat.id, 'Что-то пошло не так, начни со /start')

def circle_length_by_radius(message):
    radius = int(message.text)*2
    radius_text = str(radius)
    answer = ['Ваша длина круга:    ', radius_text, 'π', ' (см)']
    answer = ''.join(answer)
    bot.send_message(message.chat.id, answer)

def circle_length_by_diametr(message):
    diametr = int(message.text)
    diametr_text = str(diametr)
    answer = ['Ваша длина круга:    ', diametr_text, 'π', ' (см)']
    answer = ''.join(answer)
    bot.send_message(message.chat.id, answer)
    
def circle_length_by_square(message):
    square = sqrt((int(message.text)*4))
    square_text = str(square)
    answer = ['Ваша длина круга:    ', square_text, ' (см)']
    answer = ''.join(answer)
    bot.send_message(message.chat.id, answer)



def circle_square_by_smth(message):
    if message.text == 'Радиус, неизвестна площадь':
        bot.send_message(message.chat.id, 'Введите радиус(см):')
        bot.register_next_step_handler(message, circle_square_by_radius)
    elif message.text == 'Диаметр, неизвестна площадь':
        bot.send_message(message.chat.id, 'Введите диаметр(см):')
        bot.register_next_step_handler(message, circle_square_by_diametr)
    elif message.text == 'Длина, неизвестна площадь':
        bot.send_message(message.chat.id, 'Введите длину(см):')
        bot.register_next_step_handler(message, circle_square_by_length)
    else:
        bot.send_message(message.chat.id, 'Что-то пошло не так, начни со /start')

def circle_square_by_radius(message):
    radius = (int(message.text))**2
    radius_text = str(radius)
    answer = ['Ваша площадь:    ', radius_text, 'π', ' (см^2)']
    answer = ''.join(answer)
    bot.send_message(message.chat.id, answer)

def circle_square_by_diametr(message):
    diametr = (int(message.text)/2)**2
    diametr_text = str(diametr)
    answer = ['Ваша площадь:    ', diametr_text, 'π', ' (см^2)']
    answer = ''.join(answer)
    bot.send_message(message.chat.id, answer)
    
def circle_square_by_length(message):
    length = ((int(message.text))**2)/4
    length_text = str(length)
    answer = ['Ваша площадь:    ', length_text,'π', ' (см^2)']
    answer = ''.join(answer)
    bot.send_message(message.chat.id, answer)


    
bot.polling()

