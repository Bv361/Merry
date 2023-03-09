import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

# Replace YOUR_TOKEN_HERE with your actual bot token
bot = telegram.Bot(token='5998833639:AAFcAutRO89TjbGPTsOOPSxyUV7iDi5ZuX8')

members = {} # dictionary to keep track of members and their balance

def start(update, context):
    """Handler for the /start command."""
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Welcome to the Merry-go-round control bot!')

def pay(update, context):
    """Handler for the /pay command."""
    user_id = update.effective_user.id
    if user_id not in members:
        members[user_id] = 0
    members[user_id] += 10 # assuming each payment is 10 units
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Payment received. Your balance is now {} units.'.format(members[user_id]))

def show(update, context):
    """Handler for the /show command."""
    text = 'Members who have paid:\n'
    for user_id, balance in members.items():
        if balance > 0:
            user = bot.get_chat_member(chat_id=update.effective_chat.id, user_id=user_id).user
            text += '- {} (balance: {} units)\n'.format(user.full_name, balance)
    text += 'Members who have not paid:\n'
    for user_id, balance in members.items():
        if balance == 0:
            user = bot.get_chat_member(chat_id=update.effective_chat.id, user_id=user_id).user
            text += '- {} (balance: {} units)\n'.format(user.full_name, balance)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def unknown(update, context):
    """Handler for unknown commands."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I don't understand that command.")

# Create the handlers for the commands
start_handler = CommandHandler('start', start)
pay_handler = CommandHandler('pay', pay)
show_handler = CommandHandler('show', show)
unknown_handler = MessageHandler(Filters.command, unknown)

# Create the updater and add the handlers to it
updater = Updater(token='5998833639:AAFcAutRO89TjbGPTsOOPSxyUV7iDi5ZuX8', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(pay_handler)
dispatcher.add_handler(show_handler)
dispatcher.add_handler(unknown_handler)

# Start the bot
updater.start_polling()
updater.idle()
