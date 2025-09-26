import telebot
import logging
import os
import joblib
import csv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReactionTypeEmoji

# In order to run the bot, you need to set the AUTH_TOKEN environment variable with your bot's token, we do this for security reasons, so you don't expose your token in the code.
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
if not AUTH_TOKEN:
    raise ValueError("AUTH_TOKEN environment variable is not set.")

bot = telebot.TeleBot(AUTH_TOKEN)

# Here we set the logging level to CRITICAL to avoid too many logs, but we also log everything to a file named bot.log
logger = telebot.logger
logger.setLevel(logging.CRITICAL)

file_handler = logging.FileHandler("bot.log") # Log file name, it logs everything, you can check it in case of errors.
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Replace these with your actual channel and group IDs, make sure the bot is an admin in both, do not remove the '-' sign.
LOGS_CHANNEL_ID = '-123456789012'
ADMINS_GROUP_ID = '-123456789012'

# Load the trained model and vectorizer, make sure these files are in the same directory as this script.
model = joblib.load('model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# We add a detect command which will be used to detect spam messages and normal messages, it is important to log normal messages too.
user_original_message = {}
@bot.message_handler(commands=["detect"])
def spam_message(message):
    admins = bot.get_chat_administrators(message.chat.id)
    # We check for both hidden and normal admins
    if any(admin.user.id == message.from_user.id for admin in admins) or (message.sender_chat and message.sender_chat.id == message.chat.id):
        if not message.reply_to_message:
            bot.reply_to(message, "You need to reply to a message to mark it!")
            return
            
        key = (message.chat.id, message.reply_to_message.message_id)
        user_original_message[key] = message.reply_to_message.text
            
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton('Spam', callback_data=f'spam:{message.chat.id}:{message.reply_to_message.message_id}'), # Do not change the callback data, it is used in the callback handler.
            InlineKeyboardButton('Normal', callback_data=f'normal:{message.chat.id}:{message.reply_to_message.message_id}') # Do not change the callback data, it is used in the callback handler.
        )
        bot.reply_to(message, "Choose the type which fits this message. This action cannot be undone.", reply_markup=markup)
    else:
        bot.reply_to(message, "You need to be an admin to use this command!")
        
# Now a command to send the CSV file which contains the messages and their labels, only for admins.
# We assume the CSV file is named spam_messages.csv and is in the same directory as this script, so if you change anything, make sure to change it here too.
@bot.message_handler(commands=['send_data'])
def send_data(message):
    admins = bot.get_chat_administrators(message.chat.id)
    if any(admin.user.id == message.from_user.id for admin in admins) or (message.sender_chat and message.sender_chat.id == message.chat.id):
        with open('spam_messages.csv', 'r', encoding='utf-8') as file:
            data = file.read()
        if not data:
            bot.reply_to(message, "No spam messages found.")
            return
        total_amount = len(data.splitlines())
        with open('spam_messages.csv', 'rb') as f:
            bot.send_document(message.chat.id, f, caption=f"Spam message data with a total of *{total_amount}* entries.", parse_mode='Markdown')
    else:
        bot.reply_to(message, "You need to be an admin to use this command!")
        
# We also add a command to check a certain message we want by replying to it, this is useful if we want to see how our model is performing.
@bot.message_handler(commands=['check'])
def check_message(message):
    admins = bot.get_chat_administrators(message.chat.id)
    if any(admin.user.id == message.from_user.id for admin in admins) or (message.sender_chat and message.sender_chat.id == message.chat.id):
        text = message.reply_to_message.text
        X_new = vectorizer.transform([text])
        prediction = model.predict(X_new)[0]
        proba = model.predict_proba(X_new)[0]
        spam_index = list(model.classes_).index("spam")
        spam_confidence = proba[spam_index]
        if prediction  == 'spam':
            bot.reply_to(message, f"پیام مورد نظر با احتمال *{spam_confidence*100:.2f}%* اسپم شناسایی شده است.", parse_mode='Markdown')
        else:
            bot.reply_to(message, "پیام مورد نظر اسپم شناسایی نشد.")
    else:
        bot.reply_to(message, "You need to be an admin to use this command!")

# We define a function to get the username of a user and in case they don't have one, we return their user ID only.
def get_username(message):
    username = '@' + message.from_user.username + ' ' + f'(`{message.from_user.id}`)' if message.from_user.username else f'کاربر بدون نام کاربری با آیدی عددی `{message.from_user.id}`'
    return username
        
# Now we check EVERY message to see if our model detects it as spam, if it does, we send a prompt to admin groups so they can check it.
warning_messages = {}
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    if text:
        X_new = vectorizer.transform([text])
        prediction = model.predict(X_new)[0]
        proba = model.predict_proba(X_new)[0]
        spam_index = list(model.classes_).index("spam")
        spam_confidence = proba[spam_index]
        
        if prediction == 'spam' and spam_confidence > 0.4:
            username = get_username(message)
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton('⛔️ پیام اسپم ⛔️', callback_data=f'spamdetected:{message.chat.id}:{message.message_id}'), # Do not change the callback data, it is used in the callback handler.
                InlineKeyboardButton('❇️ تبلیغات ❇️', url='https://t.me/ITheEqualizer'), # Change this link to your own advertisement link, there is a link in the message too, you can change the message to your own language if you want.
            )
            
            warning_messages[(message.chat.id, message.message_id)] = bot.reply_to(message, f"""
پیام شما با احتمال **{spam_confidence*100:.2f}%** اسپم و تبلیغات شناسایی شده است و در انتظار تایید توسط ادمین است.

در صورت تمایل به سفارش تبلیغات [اینجا](https://t.me/ITheEqualizer) کلیک کنید و یا از دکمه زیر همین پیام استفاده کنید.

در صورت بررسی و عدم وجود مشکل علامت 👍 در زیر پیام شما قرار خواهد گرفت و در غیر این صورت پیام شما حذف خواهد شد.                                                                                   
                                                                                   """, parse_mode='Markdown', reply_markup=markup)
            admin_markup = InlineKeyboardMarkup()
            admin_markup.add(
                InlineKeyboardButton('بررسی پیام', url=f'https://t.me/SomeCoolGroup/{message.message_id}'), # Change this link to your own group link, only the SomeCoolGroup part.
                InlineKeyboardButton('اسپم نیست', callback_data=f'checked:{message.chat.id}:{message.message_id}'), # Do not change the callback data, it is used in the callback handler.              
            )
            bot.send_message(ADMINS_GROUP_ID, f"یک پیام احتمالی اسپم با احتمال {spam_confidence*100:.2f}% از {username} شناسایی شده است و نیازمند تایید شماست.", parse_mode='Markdown', reply_markup=admin_markup) # We define the admin's group ID at the start of the code, make sure to change it to your own group ID.
            
# In order to handle the button presses, we define a callback query handler, we also define a function to make sure only admins can click on the buttons.
def admin_check(call):
    admins = bot.get_chat_administrators(call.message.chat.id)
    return any(admin.user.id == call.from_user.id for admin in admins) or (call.sender_chat and call.sender_chat.id == call.message.chat.id)

@bot.callback_query_handler(func=admin_check)
def callback_handler(call):
    try:
        action, chat_id, msg_id = call.data.split(":")
        chat_id = int(chat_id)
        msg_id = int(msg_id)
    except ValueError:
        return    
    if action == 'spamdetected': # This part handles the spam detected button, it deletes the message and notifies the user.
        try:
            # We log the deleted message to the logs channel before deleting it, we set the channel ID at the start of the code.
            bot.send_message(LOGS_CHANNEL_ID, f"""پیام اسپم از کاربر شناسایی و حذف شد
 ادمین: {call.from_user.first_name}(`{call.from_user.id}`)     
                        
#spam""", parse_mode='Markdown')
            bot.forward_message(LOGS_CHANNEL_ID, chat_id, msg_id)
            bot.delete_message(chat_id, msg_id)
            warning_message = warning_messages.pop((chat_id, msg_id), None)
            if warning_message:
                bot.delete_message(warning_message.chat.id, warning_message.message_id)
            bot.answer_callback_query(call.id, "پیام اسپم حذف شد.", show_alert=True)
        except Exception as e:
            bot.send_message(chat_id, f"خطا در حذف پیام:\n*{e}*", parse_mode='Markdown')
            bot.answer_callback_query(call.id, "خطا در حذف پیام.", show_alert=True)
    elif action in ['spam', 'normal']:
        key = (chat_id, msg_id)
        original_message = user_original_message.pop(key, None)
        
        if not original_message:
            bot.answer_callback_query(call.id, "Message not found.")
            return
        
        with open('spam_messages.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([action, original_message])
        
        bot.edit_message_text(
            f"*{action.capitalize()}* message has been added!",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
        )
        
        bot.send_message(LOGS_CHANNEL_ID, f"""*{action.capitalize()}* message has been added!
ادمین: {call.from_user.first_name}(`{call.from_user.id}`)
                         
#flag""", parse_mode='Markdown')
        bot.forward_message(LOGS_CHANNEL_ID, chat_id, msg_id)
    elif action == 'checked':
        try:
            bot.set_message_reaction(chat_id, msg_id, reaction=[ReactionTypeEmoji(emoji="👍")]) # It doesn't support all the emojis, you can thank Telegram :)
            bot.answer_callback_query(call.id, "پیام تایید شد.", show_alert=True)
        except Exception as e:
            bot.send_message(call.message.chat.id, f"خطا در تایید پیام:\n\n*{e}*", parse_mode='Markdown')
            bot.answer_callback_query(call.id, "خطا در تایید پیام.", show_alert=True)
        
bot.infinity_polling() # We use infinity polling to keep the bot running.