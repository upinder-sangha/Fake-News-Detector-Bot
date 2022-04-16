from email import message
import os
from dotenv import load_dotenv
import telebot
from telebot import types
import PIL 
import classify
import image
import news
import preprocessing
from time import sleep


load_dotenv()

TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
bot = None


def bot_polling():
	global bot 
	print("Starting bot polling now")
	while True:
		try:
			print("New bot instance started")
			bot = telebot.TeleBot(TELEGRAM_API_KEY)
			botactions() 
			bot.polling()
		except Exception as ex: #Error in polling
			print(ex)
			print("Bot polling failed, restarting in 25 sec.")
			bot.stop_polling()
			sleep(25)
		else:
			bot.stop_polling()
			print("Bot polling loop finished")
			break


def botactions():
	@bot.message_handler(commands=['start'])
	def handle_start(message):
		bot.send_message(message.chat.id, "You're all set! \nSend me a news to check it's credibility.")

	@bot.message_handler(commands=['help'])
	def handle_help(message):
		help_message = """I can detect if the news related to covid-19 is fake or real and also provide you with a few web links to get more clarification on the news. It works for both the news in the form of text and in the form of image or screenshot. Simply send the text or screenshot of the news to get the result. 
		\n(Note - You may get the feedback for news not related to covid-19 too, but that may or may not be correct as I was only trained to classify covid-19 news.)
		\nIf you want any more information regarding the working of the bot, contact: \nupindersangha01@gmail.com \nor \nadig0902@gmail.com"""
		bot.send_message(message.chat.id, help_message)


	@bot.message_handler(content_types=['text'])
	def handle_text(message):
		bot.send_chat_action(message.chat.id, 'typing')

		result,probability = classify.predict(message.text)
		reply_to_user = "*There is a " + "%.0f" % probability + "% probability that the news you entered is "+result +".* \n\nHere are some of the articles that you can refer:"
		bot.send_message(message.chat.id, reply_to_user, parse_mode="Markdown")
		bot.send_chat_action(message.chat.id, 'typing')

		try:
			# search_results = news.google_search(preprocessing.remove_noise(message.text), num=3)
			search_results = news.advanced_google_search(preprocessing.remove_noise(message.text))
		except:
			bot.send_message(message.chat.id,"Sorry we couldn't find any relevant links")
		else:
			for search_result in search_results:
				bot.send_message(message.chat.id,search_result)


	@bot.message_handler(content_types=['photo'])
	def handle_image(message):
		bot.send_chat_action(message.chat.id, 'typing')

		extracted_text = image.extract_text(message,bot)
		bot.send_message(message.chat.id, "*Is the extracted text correct?:*", parse_mode="Markdown")

		keyboard = types.InlineKeyboardMarkup()
		button_1 = types.InlineKeyboardButton('YES',callback_data="YES")
		button_2 = types.InlineKeyboardButton('NO',callback_data='NO')
		keyboard.add(button_1, button_2)
		bot.send_message(message.chat.id, extracted_text, reply_markup=keyboard)


	@bot.callback_query_handler(func=lambda call: True)
	def handle_callback(call): # <- passes a CallbackQuery type object to your function

		if(call.data=="YES"):
			bot.answer_callback_query(call.id,text = "Processing...",show_alert=False)

			extracted_text = call.message.text
			result,probability = classify.predict(extracted_text)
			reply_to_user = "*There is a " + "%.0f" % probability + "% probability that the news you entered is "+result +".* \n\nHere are some of the articles that you can refer:"
			bot.send_message(call.message.chat.id, reply_to_user, parse_mode="Markdown")
			bot.send_chat_action(call.message.chat.id, 'typing')

			try:
				# search_results = news.google_search(preprocessing.remove_noise(message.text), num=3)
				search_results = news.advanced_google_search(preprocessing.remove_noise(extracted_text))
			except:
				bot.send_message(call.message.chat.id,"Sorry we couldn't find any relevant links")
			else:
				for search_result in search_results:
					bot.send_message(call.message.chat.id,search_result)

		else:
			bot.answer_callback_query(call.id,text = "Please manually type the correct news or simply copy the extracted text and edit it.",show_alert=True)


bot_polling()