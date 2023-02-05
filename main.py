import telebot
import wikipedia

token = # put your token!

bot = telebot.TeleBot(token)

results = []
page = ""

wikipedia.set_lang("ru")


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Хочу найти кое-что')
    bot.send_message(message.chat.id, 'Приветствую Вас, друг мой! Я - бот,'
                                      ' который ищет информацию в Wikipedia.',
                     reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
    global results
    global page
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    if message.text.lower() == 'хочу найти кое-что' or \
            message.text.lower() == "отменить ввод собственного запроса":
        keyboard.row("Хочу познать силу РАНДОМА!")
        keyboard.row("У меня есть определённый запрос")
        bot.send_message(message.chat.id, 'Введите тип запроса', reply_markup=keyboard)
    elif message.text.lower() == "хочу познать силу рандома!" or \
            message.text.lower() == "нет, другую тему":
        results = wikipedia.random(10)
        keyboard.row("Да, хочу про это почитать")
        keyboard.row("Нет, другую тему")
        keyboard.row("Придумал, что спросить")
        bot.send_message(message.chat.id, 'Великий Рандом выбрал тему:\n' +
                         results[0] + '\nВас устраивает эта тема?', reply_markup=keyboard)
    elif message.text.lower() == "да, хочу про это почитать":
        page = wikipedia.page(results[0])
        keyboard.row("Контент текстом")
        keyboard.row("Резюме текста")
        keyboard.row("Ссылка на страницу")
        bot.send_message(message.chat.id, "В каком формате хотите получть информацию?",
                         reply_markup=keyboard)
    elif message.text.lower() == "у меня есть определённый запрос" or \
            message.text.lower() == "придумал, что спросить":
        keyboard.row("Отменить ввод собственного запроса")
        bot.send_message(message.chat.id, "Введите свой запрос",
                         reply_markup=keyboard)
    elif message.text == "Ссылка на страницу":
        bot.send_message(message.chat.id, page.url)
        keyboard.row("Хочу познать силу РАНДОМА!")
        keyboard.row("У меня есть определённый запрос")
        bot.send_message(message.chat.id, "Надеюсь ответ понравился Вам!)\n"
                                          "Можете снова спросить что-нибудь",
                         reply_markup=keyboard)
    elif message.text.lower() == "контент текстом":
        f = open("text.txt", "w")
        f.write(page.content)
        f.close()
        f = open("text.txt", "r")
        bot.send_document(message.chat.id, f)
        f.close()
        keyboard.row("Хочу познать силу РАНДОМА!")
        keyboard.row("У меня есть определённый запрос")
        bot.send_message(message.chat.id, "Надеюсь ответ понравился Вам!)\n"
                                          "Можете снова спросить что-нибудь",
                         reply_markup=keyboard)
    elif message.text == "Резюме текста":
        keyboard.row("Хочу познать силу РАНДОМА!")
        keyboard.row("У меня есть определённый запрос")
        bot.send_message(message.chat.id, page.summary)
        bot.send_message(message.chat.id, "Надеюсь ответ понравился Вам!)\n"
                                          "Можете снова спросить что-нибудь",
                         reply_markup=keyboard)
    elif message.text == "1" or message.text == "2" or \
            message.text == "3" or message.text == "4" or message.text == "5":
        page = wikipedia.page(results[int(message.text)-1])
        keyboard.row("Контент текстом")
        keyboard.row("Резюме текста")
        keyboard.row("Ссылка на страницу")
        bot.send_message(message.chat.id, "В каком формате хотите получть информацию?",
                         reply_markup=keyboard)
    else:
        try:
            results = wikipedia.search(message.text)
            s = "Найденные ответы на ваш запрос:\n"
            for i in range(min(5, len(results))):
                s += str(i+1) + ". " + results[i] + '\n'
                keyboard.row(str(i+1))
            bot.send_message(message.chat.id, s)
            bot.send_message(message.chat.id, "Нажмите на номер(только номер,"
                                              " без знаков), который лучше "
                                              "подходит к вашему запросу",
                             reply_markup=keyboard)
        except:
            results = wikipedia.search(message.text)
            keyboard.row("Хочу познать силу РАНДОМА!")
            keyboard.row("У меня есть определённый запрос")
            bot.send_message(message.chat.id, "К сожалению, по запросу " + message.text +
                             " ничего не нашлось :(", reply_markup=keyboard)


bot.polling()
