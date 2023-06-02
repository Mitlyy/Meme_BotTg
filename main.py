import telebot
import requests
import random
from PIL import Image, ImageDraw, ImageFont
import urllib.request
import textwrap
import codecs

responses_name = 'Responses.txt'

def update_resp():
    global responses
    with open(responses_name, encoding = "utf8") as f:
        responses = f.readlines()
        print(responses)

update_resp()
fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 36)
TOKEN = "5807688740:AAETKlPGGY4TB1b2YI7YeZs7jvea5IDIts4"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types = ['photo'])
def handle_photo(message):
	file_id = message.photo[-1].file_id
	file_info = bot.get_file(file_id)
	file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"
	urllib.request.urlretrieve(file_url, "temp.jpg")
	with Image.open("temp.jpg") as img:
		update_resp()
		img1_resized = img.resize((571, 548))
		response = random.choice(responses)
		make_meme(img1_resized, response[0:len(response)-1])

	with open("memed.jpg", "rb") as file:
		bot.send_photo(message.chat.id, file)

def make_meme(img, text):
	img2 = Image.open("quad.jpg")
	img2.paste(img, (53, 50))
	draw = ImageDraw.Draw(img2)
	text = text
	text = textwrap.fill(text, 30)
	draw.text((60, 650), text, fill = 'white', font = fnt)
	img2.save("memed.jpg")

@bot.message_handler(commands=['add'])
def add_text(message):
    # Get the text from the message
    new_text = message.text[5:]
# Write the new text to the file
    file = codecs.open(responses_name, "a", "utf-8")
    file.write(new_text + "\n")
    bot.send_message(message.chat.id, f"Текст '{new_text}' добавлен!")

bot.polling()