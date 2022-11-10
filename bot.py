from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import ParseMode
from settings import TOKEN, HEROKU_APP
from answers import *
from handlers import *
import logging
import os


PORT = int(os.environ.get('PORT', 5000))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

DATE, PHOTO, CITY, ISTODAY, ISCITYRIGHT, WAITFEEDBACK = range(6)

def start(update, context):   
    if update.callback_query:
        query = update.callback_query
        if query.data == 'one more photo':
            query.edit_message_text(ONE_MORE_PHOTO_ANSWER)
            return PHOTO
        elif query.data == 'feedback':
            query.edit_message_text(FEEDBACK_ANSWER)
            return WAITFEEDBACK
        else:
            query.edit_message_text(ERROR_ANSWER)
            return ConversationHandler.END
    elif update.message.text == '/feedback':
        update.message.reply_text(FEEDBACK_ANSWER)
        return WAITFEEDBACK
    elif update.message.text == '/stop':
        update.message.reply_text(STOP_ANSWER)
        return ConversationHandler.END
    elif update.message.text == '/start':
        if search_user(mdb, update.message.chat.id):
            update.message.reply_text(WELCOME_BACK_ANSWER)
            return PHOTO
        else:
            update.message.reply_text(HI_ANSWER, ParseMode.MARKDOWN, disable_web_page_preview=True)
            # context.job_queue.run_repeating(seeYa, interval=1, first=300, context=update.message.chat_id)
            return PHOTO
    else:
        update.message.reply_text(STOP_ANSWER)
        return ConversationHandler.END

# def seeYa(context):
#     chat_id=context.job.context
#     context.bot.send_message(chat_id=chat_id, 
#                              text="Вы еще тут?")

def stop(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=STOP_ANSWER)
    return ConversationHandler.END

def error(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=ERROR_ANSWER)
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater(TOKEN, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler(["start", "stop", "feedback"], start), CallbackQueryHandler(start), MessageHandler(Filters.all, start)],
        states={
            DATE: [CommandHandler(["start", "feedback", "cancel"], waitDate), MessageHandler(Filters.text & (~ Filters.command), recieveDate), MessageHandler(Filters.all & (~ Filters.text) & (~ Filters.command), waitDate)],
            CITY: [CommandHandler(["start", "feedback", "cancel"], waitCity), MessageHandler(Filters.text & (~ Filters.command), recieveCity), MessageHandler(Filters.all & (~ Filters.text) & (~ Filters.command), waitCity)],
            PHOTO: [CommandHandler(["start", "feedback", "cancel"], waitPhoto, pass_job_queue=True), MessageHandler(Filters.photo, recievePhoto, pass_job_queue=True), MessageHandler(Filters.all & (~ Filters.photo) & (~ Filters.command), waitPhoto, pass_job_queue=True)],
            ISTODAY: [CommandHandler(["start", "feedback", "cancel"], waitAnswerForDate), CallbackQueryHandler(isToday), MessageHandler(Filters.all & (~ Filters.command), waitAnswerForDate)],
            ISCITYRIGHT: [CommandHandler(["start", "feedback", "cancel"], waitAnswerForCity), CallbackQueryHandler(isCityRight), MessageHandler(Filters.all  & (~ Filters.command), waitAnswerForCity)],
            WAITFEEDBACK: [CommandHandler("cancel", cancelFeedback), MessageHandler(Filters.text, recieveFeedback), MessageHandler(Filters.all & (~ Filters.text) & (~ Filters.command), waitFeedback)]
        },
        fallbacks=[CommandHandler("stop", stop)],
    )

    dp.add_handler(conv_handler)
    
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook(HEROKU_APP + TOKEN)

    updater.idle()

if __name__ == '__main__':
    main()