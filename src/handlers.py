from telegram import InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from mongodb import mdb, search_or_save_user, add_date, add_city, search_user, add_feedback
from settings import TG_CHATID
from validations import checkDate
from keyboards import *
from answers import *
import datetime

DATE, PHOTO, CITY, ISTODAY, ISCITYRIGHT, WAITFEEDBACK = range(6)

def recievePhoto(update, context):
    fileID = update.message['photo'][-1]['file_id']
    userID = update.message.chat.id
    search_or_save_user(mdb, userID, fileID)
    update.message.reply_text(AWESOME_PHOTO_ANSWER, reply_markup=InlineKeyboardMarkup(isTodayKeyboard))
    return ISTODAY

def recieveCity(update, context):
    userID = update.message.chat.id
    city = update.message.text
    add_city(mdb, userID, city)
    user = search_user(mdb, userID)
    date = user['date']
    city = user['city']
    
    context.bot.sendPhoto(chat_id = TG_CHATID,
                            caption = f'{date}\n{city.title()}',
                            photo = user['file_id'])
    update.message.reply_text(BYE_ANSWER, reply_markup=InlineKeyboardMarkup(finalKeyboard))
    return ConversationHandler.END

def recieveDate(update, context):
    userID = update.message.chat.id
    date = update.message.text
    result = checkDate(date)

    if result == 'old':
        update.message.reply_text(OLD_PHOTO_ANSWER)
        return DATE
    elif result == 'future':
        update.message.reply_text(PHOTO_FROM_FUTURE_ANSWER)
        return DATE
    elif result == 'error':
        update.message.reply_text(USE_FORMAT_ANSWER)
        return DATE
    else:
        add_date(mdb, userID, date)
        user = search_user(mdb, userID)

        if user['city']:
            city = user['city']
            update.message.reply_text(f"Подскажи, это город {city.title()}?", reply_markup=InlineKeyboardMarkup(isCityCorrectKeyboard))
            return ISCITYRIGHT
        elif not user['city']:
            update.message.reply_text(SEND_CITY_ANSWER)
            return CITY
        else:
            update.message.reply_text(NO_PHOTO_ANSWER)
            return PHOTO

def recieveFeedback(update, context):
    feedback = update.message.text
    add_feedback(mdb, feedback)
    update.message.reply_text(THANKS_FOR_FEEDBACK_ANSWER, reply_markup=InlineKeyboardMarkup(finalKeyboardAfterFeedback))
    return ConversationHandler.END

def cancelFeedback(update, context):
    update.message.reply_text(THANKS_FOR_FEEDBACK_ANYWAY_ANSWER, reply_markup=InlineKeyboardMarkup(finalKeyboardAfterFeedback))
    return ConversationHandler.END

def isToday(update, context):
    query = update.callback_query
    userID = query.message.chat.id
    date = (datetime.datetime.now() + datetime.timedelta(hours=3)).strftime('%d.%m.%Y')
    user = search_user(mdb, userID)

    if query.data == 'today' and user['city']:
        add_date(mdb, userID, date)
        query.edit_message_text(text=f"Подскажи, это город {user['city'].title()}?", reply_markup=InlineKeyboardMarkup(isCityCorrectKeyboard))
        return ISCITYRIGHT
    elif query.data == 'today' and not user['city']:
        add_date(mdb, userID, date)
        query.edit_message_text(text=SEND_CITY_ANSWER)
        return CITY
    else:
        query.edit_message_text(text=SEND_DATE_ANSWER)
        return DATE

def isCityRight(update, context):
    query = update.callback_query
    userID = query.message.chat.id

    if query.data == 'cityCorrect':
        user = search_user(mdb, userID)
        date = user['date']
        city = user['city']
        context.bot.sendPhoto(chat_id = TG_CHATID,
                              caption = f'{date}\n{city.title()}',
                              photo = user['file_id'])
        query.edit_message_text(text=BYE_ANSWER, reply_markup=InlineKeyboardMarkup(finalKeyboard))
        return ConversationHandler.END
    else:
        query.edit_message_text(text=SEND_NEW_CITY_ANSWER)
        return CITY

def waitDate(update, context):
    update.message.reply_text(WAIT_DATE_ANSWER)
    return DATE

def waitPhoto(update, context):
    update.message.reply_text(WAIT_PHOTO_ANSWER)
    return PHOTO

def waitCity(update, context):
    update.message.reply_text(WAIT_CITY_ANSWER)
    return CITY

def waitAnswerForCity(update, context):
    update.message.reply_text(WAIT_CALLBACK_ANSWER)
    return ISCITYRIGHT

def waitAnswerForDate(update, context):
    update.message.reply_text(WAIT_CALLBACK_ANSWER)
    return ISTODAY

def waitFeedback(update, context):
    update.message.reply_text(WAIT_FEEDBACK_ANSWER)
    return WAITFEEDBACK