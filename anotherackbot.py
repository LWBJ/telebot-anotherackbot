from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os

def ack(bot, update):
  #Takes in the command /ack with a message after a space. Will ask for a proper message if none is provided
  #Responds with a message containing the message, a header "names" and an inline keyboard
  #This message will be updated with new names every time the button is pressed

  info = update.message.text.partition(' ')
  
  if info[2] == "":
    update.message.reply_text(text="Please add a message after /ack!")
  else:
    new_message = info[2] + "\n\nRespondents:\n\nTotal: 0"

    keyboard = [InlineKeyboardButton("Acknowledged", callback_data=1)],
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(text=new_message, reply_markup=reply_markup)

def messagechange(mes, new_name):
  #Takes in original message and a new name to return a message with the new name, increase in total number and keep formatting

  i = 1
  new_mes=mes
  while i <= len(mes):
    reg = mes[-i:-i+9]
    if reg == "\n\nTotal: ":
      s1 = mes[:-i]
      num = str(int(mes[-i+9:]) + 1)
      new_mes = s1 + "\n" + new_name + reg + num
      i = len(mes)      
    i += 1
  return new_mes    

def button(bot, update):
  #The button creates an updated message and recreates the same inline keyboard
  #The username of the respondent is extracted and compared against the existing message
  #If the username is already there, a notification is sent saying the response is already recorded
  #Else, the message is updated with a new name and a notification is sent out
  
  query = update.callback_query
  og_message = query.message.text
  
  keyboard = [InlineKeyboardButton("Acknowledged", callback_data=1)],
  same_markup = InlineKeyboardMarkup(keyboard)
  
  new_name = query.from_user['first_name'] + ' ' + query.from_user['last_name']
  
  if new_name in og_message:
    query.answer(text="Response already recorded!")
  else:
    new_message = messagechange(og_message,new_name)
    query.edit_message_text(reply_markup=same_markup, text=new_message)
    query.answer(text="Thank you for your response!")

def start(bot, update):
  update.message.reply_text(text="Hello! This is AnotherAckBot, a hobbyist recreation of acknowledgedbot. I send notifications after a response and track the total number of responses.")

def helpfunc(bot, update):
  the_message = """Available commands:

/help - this command
/ack - starts a new ack list

Add your message after a space following /ack. For example:

/ack My message"""
  update.message.reply_text(text=the_message)

def main():
  TOKEN = os.environ.get('API_KEY','')
  NAME = "anotherackbot"
  PORT = os.environ.get('PORT')
  
  updater = Updater(token=TOKEN)
  dp = updater.dispatcher

  dp.add_handler(CommandHandler("ack",ack))
  dp.add_handler(CallbackQueryHandler(button))
  dp.add_handler(CommandHandler("start",start))
  dp.add_handler(CommandHandler("help",helpfunc))

  #updater.start_polling()
  updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
  updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
  
if __name__ == "__main__":
  main()
