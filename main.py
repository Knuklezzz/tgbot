import telebot
from telebot import types
import requests
from currency_converter import CurrencyConverter
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import os
import re

bot = telebot.TeleBot('6712197035:AAGQQh4ZXRQvk_Y9ff3gDtTeVkZAiG6I3YI')

URL = 'https://api.exchangerate-api.com/v4/latest/EUR'

response = requests.get(URL)
data = response.json()
rateEurRub = data['rates']['RUB']
rateEurCny = data['rates']['CNY']
rateCnyRub = rateEurRub/rateEurCny
ourRate = rateCnyRub + rateCnyRub * 0.0595
print(ourRate)

currency = CurrencyConverter()
comm = 0.15
course = 13.35 #берем +5,95% от биржи гугл
prev_message = {}
prevbot_message = {}
sentm = ''
weight = 0
size = 0
link = ''
price = 0
priceCny = 0
photo1 = ''
last_sent_photos = {}
name = ''
number = ''
address = ''
promo_codes = ['egorny', 'nikitos']


# Папка для хранения сообщений
messages_folder = 'user_messages'

# Если папка не существует, создайте ее
if not os.path.exists(messages_folder):
    os.makedirs(messages_folder)

# Папка для хранения фотографий
photos_folder = 'user_photos'

# Папка для хранения путей к фотографиям
paths_folder = 'photo_paths'

# Если папки не существуют, создайте их
if not os.path.exists(photos_folder):
    os.makedirs(photos_folder)

if not os.path.exists(paths_folder):
    os.makedirs(paths_folder)

@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)  # Можно указать количество кнопок в ряду

    button1 = types.InlineKeyboardButton("Оформить заказ", callback_data='button_order')
    button2 = types.InlineKeyboardButton("Калькулятор стоимости", callback_data='button_calc')
    button3 = types.InlineKeyboardButton("Каталог", callback_data='button_catalogue')

    markup.add(button1, button2, button3)

    bot.send_message(message.chat.id, f'<b>😉Добро пожаловать в бот группы LOGISTIX!</b>\n\n'
                                f'Уже 1.5 года помогаем Вам заказывать товары с <b>POIZON</b>',
                                # f'<b>-POIZON (DEWU)</b>\n'
                                # f'<b>-END CLOTHING</b>\n'
                                # f'<b>-YOOX</b>\n'
                                # f'<b>-И ДРУГИЕ</b>\n',
                                parse_mode="HTML", reply_markup = markup)



@bot.callback_query_handler(func=lambda call: True)
def handle_inline_button(callback_query):
        global sentm
        global weight
        global size
        global link
        print(callback_query.data)
        if callback_query.data == 'button_order':
            markup = types.InlineKeyboardMarkup(row_width=1)  # Можно указать количество кнопок в ряду
            button1 = types.InlineKeyboardButton("Утепленные кроссовки / Ботинки", callback_data='button_order1')
            button2 = types.InlineKeyboardButton("Кеды / Кроссовки / Легкая обувь", callback_data='button_order2')
            button3 = types.InlineKeyboardButton("Куртки", callback_data='button_order3')
            button4 = types.InlineKeyboardButton("Футболки / Лонгсливы", callback_data='button_order4')
            button5 = types.InlineKeyboardButton("Худи / Cвитшоты", callback_data='button_order5')
            button6 = types.InlineKeyboardButton("Штаны / Брюки / Джинсы", callback_data='button_order6')
            button7 = types.InlineKeyboardButton("Аксессуары", callback_data='button_order7')
            markup.add(button1, button2, button3, button4, button5, button6, button7)
            bot.send_message(callback_query.message.chat.id, 'Выберите категорию товара', reply_markup=markup)
            bot.answer_callback_query(callback_query.id)

        elif callback_query.data == 'button_calc':
            sentm = 'Введите стоимость в ¥'
            bot.send_message(callback_query.message.chat.id, "Введите стоимость в ¥")
            bot.answer_callback_query(callback_query.id)

        elif callback_query.data == 'button_catalogue':
            bot.send_message(callback_query.message.chat.id, "В разрабоке...")
            bot.answer_callback_query(callback_query.id)

        if callback_query.data == 'start':
            handle_start(callback_query.message)
            bot.answer_callback_query(callback_query.id)

        if callback_query.data == 'button_order1':
            weight = 2000
            print(weight)
        elif callback_query.data == 'button_order2':
            weight = 1500
            print(weight)
        elif callback_query.data == 'button_order3':
            weight = 2000
            print(weight)
        elif callback_query.data == 'button_order4':
            weight = 1300
            print(weight)
        elif callback_query.data == 'button_order5':
            weight = 1500
            print(weight)
        elif callback_query.data == 'button_order6':
            weight = 1500
            print(weight)
        elif callback_query.data == 'button_order7':
            weight = 1000
            print(weight)

        if callback_query.data == 'button_order1' or callback_query.data == 'button_order2' or callback_query.data == 'button_order3' or callback_query.data == 'button_order4' or callback_query.data == 'button_order5' or callback_query.data == 'button_order6' or callback_query.data == 'button_order7':
            print('gbfdf')
            sentm = 'фотка'
            bot.send_message(callback_query.message.chat.id, '🖼Пожалуйста, вставьте фото товара, как показано на примере:')
            bot.answer_callback_query(callback_query.id)

        if callback_query.data ==  'button_confirm1':
            sentm = 'Карточка верна'
            bot.send_message(callback_query.message.chat.id,'👶Пожалуйста, введите ФИО полностью как в паспорте (например Иванов Иван Иванович):')
            sentm = 'Ждем ФИО'
            bot.answer_callback_query(callback_query.id)


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    global ourRate
    global comm
    global sentm
    global size
    global link
    global price
    global priceCny
    global name
    global number
    global address
    global promo_codes

    user_id = str(message.from_user.id)
    user_message = message.text
    hide_markup = types.ReplyKeyboardRemove()

    # Создаем файл для каждого пользователя
    user_filename = os.path.join(messages_folder, f'{user_id}.txt')

    if message.text.isdigit() and sentm == 'Введите стоимость в ¥':
        inttext = int(message.text)
        res = inttext * ourRate + inttext * ourRate * comm + weight
        res = int(res) + bool(res % 1)
        mess = f'{res}'
        bot.send_message(message.chat.id, 'К оплате: '+ mess + '₽')
        sentm = ''

    elif sentm == 'Введите стоимость в ¥':
        bot.send_message(message.chat.id, 'Неверный формат, введите стоимость')

    elif sentm == 'Фотография принята':
        link_to_check = user_message
        check_mask = re.compile(r'^https://dw4.co/t/A/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8}$')
        result = check_mask.match(link_to_check)

        if result:
            with open(user_filename, 'a') as file:
                file.write('Link: ' + user_message + '\n')
            bot.send_message(message.chat.id, "Ссылка принята")
            sentm = 'Ссылка принята'
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            item1 = types.KeyboardButton("Пропустить")
            keyboard.add(item1)
            bot.send_message(message.chat.id, "📏Укажите размер или комплектность. Если у Вашего товара нет такого выбора - нажмите 'Пропустить'", reply_markup=keyboard)
            link = link_to_check

        else:
            bot.send_message(message.chat.id, "Ошибка! Введенная ссылка не соответсвует маске ввода. Попробуйте еще раз")

    elif sentm == 'Ссылка принята':
        with open(user_filename, 'a') as file:
            file.write('Size: ' + user_message + '\n')
        bot.send_message(message.chat.id, "Принято", reply_markup=hide_markup)
        sentm = 'Размер принят'
        bot.send_message(message.chat.id, "⚠️ Введите стоимость выбранной вещи В ЮАНЯХ (зачеркнутая цена).⛔️⛔️ Если Вы рассчитали или оплатили неверную сумму или заказали по ≈ то будет сделан возврат средств в течении 10 рабочих дней БЕЗ возможности доплаты! ⛔️⛔️")
        size = user_message

    elif sentm == 'Размер принят' and message.text.isdigit():
        if size == 'Пропустить':
            size = '-'
        with open(user_filename, 'a') as file:
            file.write(user_message + '\n')
        priceCny = int(message.text)
        price = priceCny * ourRate + priceCny * ourRate * comm + weight
        price = int(price) + bool(price % 1)
        #price = f'{price}'
        #bot.send_message(message.chat.id, 'К оплате: ' + price + '₽')
        sentm = ''
        admin_user_id = '6173381955'  # Замените на ID вашего администратора
        if user_id in last_sent_photos:
            # Отправляем последнюю сохраненную фотографию
            with open(last_sent_photos[user_id], 'rb') as photo:
                markup = types.InlineKeyboardMarkup(row_width=1)  # Можно указать количество кнопок в ряду
                button1 = types.InlineKeyboardButton("Все верно", callback_data='button_confirm1')
                button2 = types.InlineKeyboardButton("Изменить", callback_data='button_decline1')
                markup.add(button1, button2)
                bot.send_photo(user_id, photo, caption=f'<b>Ссылка: </b> {link}\n'
                                            f'<b>Размер или комплектность: </b> {size}\n'
                                            f'<b>Стоимость в ¥: </b> {priceCny}\n'
                                            f'<b>Стоимость в ₽: </b> {price}\n', parse_mode="HTML", reply_markup = markup)
                


        # bot.send_message(message.chat.id, f'<b>Ссылка на товар: </b> {link}\n'
        #                                    f'<b>Размер или комлпектность: </b> {size}\n'
        #                                    f'<b>Стоимость в ¥: </b> {priceCny}\n'
        #                                    f'<b>Стоимость в ₽, с учетом доставки по России: </b> {price}\n', parse_mode="HTML")
        # bot.send_photo(message.chat.id, photo1)#caption =  f'<b>Ссылка на товар: </b> {link}\n'
                                           #f'<b>Размер или комлпектность: </b> {size}\n'
                                           #f'<b>Стоимость в ¥: </b> {priceCny}\n'
                                           #f'<b>Стоимость в ₽, с учетом доставки по России: </b> {price}\n', parse_mode="HTML")
        #admin_message = f'Новый заказ от пользователя {user_id}:\n\n{user_message}'
        # bot.send_message(admin_user_id, f'Новый заказ от пользователя {user_id}!\n'
        #                                   f'<b>Ссылка на товар: </b> {link}\n'
        #                                   f'<b>Размер или комлпектность: </b> {size}\n'
        #                                   f'<b>Стоимость в ¥: </b> {priceCny}\n'
        #                                   f'<b>Стоимость в ₽, с учетом доставки по России: </b> {price}\n', parse_mode="HTML")

    elif sentm == 'Размер принят':
        bot.send_message(message.chat.id, 'Неверный формат, введите стоимость')

    elif sentm == 'Ждем ФИО':
        name = user_message
        bot.send_message(message.chat.id, 'Пожалуйста, введите номер телефона в формате +79998887766:')
        sentm = 'Ждем номер'

    elif sentm == 'Ждем номер':
        num_to_check = user_message
        num_mask = re.compile(r'^\+79\d{9}$')
        result = num_mask.match(num_to_check)

        if result:
            # with open(user_filename, 'a') as file:
            #     file.write('Link: ' + user_message + '\n')
            number = num_to_check
            bot.send_message(message.chat.id, "Пожалуйста, введите адрес пункта выдачи СДЭК в формате (Страна, Область, Город, Улица, Номер дома):")
            sentm = 'Ждем адрес'

        else:
            bot.send_message(message.chat.id,"Ошибка! Введенный номер не соответсвует маске ввода. Попробуйте еще раз")

    elif sentm == 'Ждем адрес':
        address = user_message
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        item1 = types.KeyboardButton("Пропустить")
        keyboard.add(item1)
        bot.send_message(message.chat.id,"Введите промокод. Если у Вас нет промокода - нажмите 'Пропустить'", reply_markup=keyboard)
        sentm = 'Ждем промокод'

    elif sentm == 'Ждем промокод':
        if user_message in promo_codes:
            bot.send_message(message.chat.id,"Супер! Скидка 5% на комиссию применена", reply_markup=hide_markup)
            comm = comm - 0.05
            price = priceCny * ourRate + priceCny * ourRate * comm + weight
            price = int(price) + bool(price % 1)
            if user_id in last_sent_photos:
                # Отправляем последнюю сохраненную фотографию
                with open(last_sent_photos[user_id], 'rb') as photo:
                    markup = types.InlineKeyboardMarkup(row_width=1)  # Можно указать количество кнопок в ряду
                    button1 = types.InlineKeyboardButton("Все верно", callback_data='button_confirm1')
                    button2 = types.InlineKeyboardButton("Изменить", callback_data='button_decline1')
                    markup.add(button1, button2)
                    bot.send_photo(user_id, photo, caption=f'<b>Ссылка: </b> {link}\n'
                                                           f'<b>Размер или комплектность: </b> {size}\n'
                                                           f'<b>Стоимость в ¥: </b> {priceCny}\n'
                                                           f'<b>Стоимость в ₽: </b> {price}\n'
                                                           f'<b>ФИО получателя: </b> {name}\n'
                                                           f'<b>Номер телефона: </b> {number}\n'
                                                           f'<b>Адрес ПВЗ: </b> {address}\n'
                                   , parse_mode="HTML",
                                   reply_markup=hide_markup)
        elif user_message == 'Пропустить':
            if user_id in last_sent_photos:
                # Отправляем последнюю сохраненную фотографию
                with open(last_sent_photos[user_id], 'rb') as photo:
                    markup = types.InlineKeyboardMarkup(row_width=1)  # Можно указать количество кнопок в ряду
                    button1 = types.InlineKeyboardButton("Все верно", callback_data='button_confirm1')
                    button2 = types.InlineKeyboardButton("Изменить", callback_data='button_decline1')
                    markup.add(button1, button2)
                    bot.send_photo(user_id, photo, caption=f'<b>Ссылка: </b> {link}\n'
                                                           f'<b>Размер или комплектность: </b> {size}\n'
                                                           f'<b>Стоимость в ¥: </b> {priceCny}\n'
                                                           f'<b>Стоимость в ₽: </b> {price}\n'
                                                           f'<b>ФИО получателя: </b> {name}\n'
                                                           f'<b>Номер телефона: </b> {number}\n'
                                                           f'<b>Адрес ПВЗ: </b> {address}\n'
                                   , parse_mode="HTML",
                                   reply_markup=hide_markup)
        else:
            bot.send_message(message.chat.id, "Не нашел такого промокода. Введите еще раз, или нажмите 'Пропустить'")


    else:
        sentm = ''
        markup = types.InlineKeyboardMarkup(row_width=1)  # Можно указать количество кнопок в ряду
        button1 = types.InlineKeyboardButton("В начало", callback_data='start')
        markup.add(button1)
        bot.send_message(message.chat.id, 'Я еще не знаю, как отвечать на эту команду :(', reply_markup = markup)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    global sentm
    global photo1
    if sentm == 'фотка':
        user_id = str(message.from_user.id)
        file_id = message.photo[-1].file_id

        # Получаем информацию о фотографии
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path

        # Сохраняем фотографию
        photo_file = bot.download_file(file_path)
        photo_filename = os.path.join(photos_folder, f'{user_id}_{file_id}.jpg')
        with open(photo_filename, 'wb') as file:
            file.write(photo_file)
        last_sent_photos[user_id] = photo_filename

        # Записываем путь к фотографии в файл
        # paths_filename = os.path.join(paths_folder, f'{user_id}_paths.txt')
        # with open(paths_filename, 'a') as file:
        #     file.write(photo_filename + '\n')
        #     photo1 = photo_filename
        # Отправляем ответное сообщение
        bot.send_message(message.chat.id, "Фотография принята")
        sentm = 'Фотография принята'
        bot.send_message(message.chat.id,'🔗Пожалуйста, отправьте ссылку на товар в нужном формате https://dw4.co/t/A/18KfFHsf:')

        #admin_user_id = '6173381955'  # Замените на ID вашего администратора
        #admin_message = f'Новая фотография от пользователя {user_id}:\n{photo_filename}'
        #with open(photo_filename, 'rb') as photo:
        #   bot.send_message(admin_user_id, admin_message)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)  # Можно указать количество кнопок в ряду
        button1 = types.InlineKeyboardButton("В начало", callback_data='start')
        markup.add(button1)
        bot.send_message(message.chat.id, 'Поставлю себе на обои 😉', reply_markup=markup)

bot.polling(none_stop=True)