import telebot
from bot_logic import gen_pass, gen_emodji, flip_coin  # Импортируем функции из bot_logic
import model # Импортируем функцию для определения породы котов из model

# Замени 'TOKEN' на токен твоего бота
bot = telebot.TeleBot("TOKEN")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши команду /info, /hello, /bye, /pass, /emodji или /coin  ")

@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "Этот бот может генерировать пароли, эмоджи, подбрасывать монеткум и определять породы котов. Просто используй команды /pass, /emodji, /coin и /cat соответственно.")

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['pass'])
def send_password(message):
    password = gen_pass(10)  # Устанавливаем длину пароля, например, 10 символов
    bot.reply_to(message, f"Вот твой сгенерированный пароль: {password}")

@bot.message_handler(commands=['emodji'])
def send_emodji(message):
    emodji = gen_emodji()
    bot.reply_to(message, f"Вот эмоджи': {emodji}")

@bot.message_handler(commands=['coin'])
def send_coin(message):
    coin = flip_coin()
    bot.reply_to(message, f"Монетка выпала так: {coin}")
    
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    if file_info.file_path:
        file_name = file_info.file_path.split('/')[-1]
        downloaded_file = bot.download_file(file_info.file_path)
        with open("image/" + file_name, 'wb') as f:
            f.write(downloaded_file)
            
        cat = model.get_class("keras_model.h5", "labels.txt", "image/" + file_name)  # Вызываем функцию для определения породы котов 
        bot.reply_to(message, "Фото сохранено!")
        bot.reply_to(message, "Порода кота: " + str(cat[0]) + " с вероятностью " + str(cat[1] * 100) + "%")  # Отправляем пользователю результат определения породы кота

# Запускаем бота
bot.polling()