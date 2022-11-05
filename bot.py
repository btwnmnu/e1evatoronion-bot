import logging
import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
import os

PORT = int(os.environ.get('PORT', 5000))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = ''
filesDict = {}
DATE, PHOTO, CITY, ISTODAY, CHANGECITY, ISCITYRIGHT = range(6)

def start(update, context):   
    if update.callback_query:
        query = update.callback_query
        if query.data == 'one more photo':
            query.edit_message_text("Присылай фото :)")
            return PHOTO
        else:
            return PHOTO
    else:
        update.message.reply_text("Привет! Я помогу отправить твое фото в канал [Лифтолук](https://t.me/e1evatoronion), пришли мне его в ответ на это сообщение :)", ParseMode.MARKDOWN, disable_web_page_preview=True)
        return PHOTO

def recievePhoto(update, context):
    global filesDict

    fileID = update.message['photo'][-1]['file_id']
    userID = update.message.chat.id
    
    if filesDict.get(userID):
        filesDict[userID]['file'] = fileID
        filesDict[userID]['date'] = None
    else:
        newElement = {userID: {'file':fileID, 'city':None, 'date' : None}}
        filesDict.update(newElement)
    
    keyboard = [
        [
            # ПОДУМАТЬ ЧТО ДОБАВИТЬ ЧТОБЫ УБРАТЬ СЛОВО "ЗАГРУЗКА"
            InlineKeyboardButton("Да", callback_data="today"),
            InlineKeyboardButton("Нет", callback_data="notToday"),
        ]
    ]
    update.message.reply_text('Как всегда великолепно!\nСегодняшнее фото?', reply_markup=InlineKeyboardMarkup(keyboard))
    return ISTODAY

def keyboard_today_callback(update, context):
    global filesDict

    query = update.callback_query
    userID = query.message.chat.id

    if query.data == 'today' and filesDict[userID]['city']:
        date = (datetime.datetime.now() + datetime.timedelta(hours=3)).strftime('%d.%m.%Y')
        filesDict[userID]['date'] = date
        keyboard = [
            [InlineKeyboardButton("Да", callback_data='cityCorrect'),
            InlineKeyboardButton("Нет", callback_data="cityWrong")]
        ]
        city = filesDict[userID]['city']
        query.edit_message_text(text=f"Подскажи, это город {city.title()}?", reply_markup=InlineKeyboardMarkup(keyboard))
        return ISCITYRIGHT
    elif query.data == 'today' and filesDict[userID]['city'] == None:
        date = (datetime.datetime.now() + datetime.timedelta(hours=3)).strftime('%d.%m.%Y')
        filesDict[userID]['date'] = date
        query.edit_message_text(text=f"Клёва! Подскажи город, в котором сделано это фото")
        return CITY
    else:
        query.edit_message_text(text=f'Напиши пожалуйста, когда было снято фото, в формате DD.MM.YYYY')
        return DATE

def isCityRight(update, context):
    global filesDict

    query = update.callback_query
    userID = query.message.chat.id

    if query.data == 'cityCorrect':
        date = filesDict[userID]['date']
        city = filesDict[userID]['city']
        context.bot.sendPhoto(chat_id = -1001514609298,
                              caption = f'{date}\n{city.title()}',
                              photo = filesDict[userID]['file'])
        filesDict[userID]['file'] = None
        filesDict[userID]['date'] = None
        keyboard = [
            [InlineKeyboardButton("Посмотреть в Лифтолук", url='https://t.me/e1evatoronion')],
            [InlineKeyboardButton("Отправить еще фото", callback_data="one more photo")],
        ]
        query.edit_message_text(text=f"Отправляю собирать лайки :)", reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END
    else:
        query.edit_message_text(text=f"Пришли пожалуйста название города в ответ")
        return CHANGECITY

def cityChanged(update, context):
    global filesDict

    userID = update.message.chat.id
    filesDict[userID]['city'] = update.message.text
    city = filesDict[userID]['city']

    if filesDict[userID]['city'] and filesDict[userID]['file'] and filesDict[userID]['date']:
        date = filesDict[userID]['date']
        city = filesDict[userID]['city']
        context.bot.sendPhoto(chat_id = -1001514609298,
                            caption = f'{date}\n{city.title()}',
                            photo = filesDict[userID]['file'])
        filesDict[userID]['file'] = None
        filesDict[userID]['date'] = None
        keyboard = [
            [InlineKeyboardButton("Посмотреть в Лифтолук", url='https://t.me/e1evatoronion')],
            [InlineKeyboardButton("Отправить еще фото", callback_data="one more photo")],
        ]
        update.message.reply_text("Отправляю собирать лайки :)", reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END
    else:
        update.message.reply_text("Что-то пошло не так, попробуй еще раз: /start")
        filesDict.clear()
        return ConversationHandler.END

def recieveCity(update, context):
    global filesDict

    userID = update.message.chat.id
    filesDict[userID]['city'] = update.message.text
    city = filesDict[userID]['city']

    if filesDict[userID]['city'] and filesDict[userID]['file'] and filesDict[userID]['date']:
        date = filesDict[userID]['date']
        city = filesDict[userID]['city']
        context.bot.sendPhoto(chat_id = -1001514609298,
                            caption = f'{date}\n{city.title()}',
                            photo = filesDict[userID]['file'])
        filesDict[userID]['file'] = None
        filesDict[userID]['date'] = None
        keyboard = [
            [InlineKeyboardButton("Посмотреть в Лифтолук", url='https://t.me/e1evatoronion')],
            [InlineKeyboardButton("Отправить еще фото", callback_data="one more photo")],
        ]
        update.message.reply_text("Отправляю собирать лайки :)", reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END
    else:
        update.message.reply_text("Что-то пошло не так, попробуй еще раз:\n/start")
        filesDict.clear()
        return ConversationHandler.END

def recieveDate(update, context):
    global filesDict

    date = update.message.text
    userID = update.message.chat.id

    if filesDict[userID]['city']:
        filesDict[userID]['date'] = date
        keyboard = [
            [InlineKeyboardButton("Да", callback_data='cityCorrect'),
            InlineKeyboardButton("Нет", callback_data="cityWrong")]
        ]
        city = filesDict[userID]['city']
        update.message.reply_text(f"Подскажи, это город {city.title()}?", reply_markup=InlineKeyboardMarkup(keyboard))
        return ISCITYRIGHT
    elif filesDict[userID]['city'] == None:
        filesDict[userID]['date'] = date
        update.message.reply_text('Подскажи пожалуйста город, в котором сделано фото')
        return CITY
    else:
        update.message.reply_text('Хм, не могу найти фотографию. Попробуй пожалуйста отправить фото снова')
        return PHOTO

def cancel(update, context):
    update.message.reply_text("Что-то пошло не так, попробуй еще раз:\n/start")
    return ConversationHandler.END

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater(TOKEN, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), CallbackQueryHandler(start)],
        states={
            DATE: [MessageHandler(Filters.regex('^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$'), recieveDate)],
            CITY: [MessageHandler(Filters.text, recieveCity)],
            PHOTO: [MessageHandler(Filters.photo, recievePhoto)],
            ISTODAY: [CallbackQueryHandler(keyboard_today_callback)],
            ISCITYRIGHT: [CallbackQueryHandler(isCityRight)],
            CHANGECITY: [MessageHandler(Filters.text, cityChanged)]
        },
        fallbacks=[CommandHandler("restart", cancel)],
    )

    dp.add_handler(conv_handler)
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://e1evatoronion-bot.herokuapp.com/' + TOKEN)

    updater.idle()


if __name__ == '__main__':
    main()
