import logging
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import requests
from bs4 import BeautifulSoup

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to parse buttons from the website
def parse_buttons(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    buttons = []
    # Find buttons on the website and extract their text and URL
    for button in soup.find_all('button'):
        text = button.text.strip()
        url = button.get('href')
        if url:
            buttons.append((text, url))
    return buttons

# Token of your bot obtained from BotFather
TOKEN = '7092119997:AAF1X1K4l_KXVyI-rEItZWRq7TEtwuhIRuU'
bot = telegram.Bot(token=TOKEN)

# Dictionary containing movie genres and their links
genres_movies = {
    'БОЙОВИКИ': 'Link to action movies',
    'ЕКШН': 'Link to action movies',
    'КОМЕДІЯ': 'Link to comedy movies',
    'ЖАХИ': 'Link to horror movies',
    'ДРАМА': 'Link to drama movies',
    'ФАНТАСТИКА': 'Link to sci-fi movies',
    'ФЕНТЕЗІ': 'Посилання на фентезійні фільми',  # Зміна 1: Додавання нового жанру
    'ДЕТЕКТИВИ': 'Посилання на детективні фільми',  # Зміна 2: Зміна тексту кнопок
    'МЕЛОДРАМИ': 'Посилання на мелодраматичні фільми',  # Зміна 2: Зміна тексту кнопок
    'ТРИЛЕРИ': 'Посилання на трилери',  # Зміна 2: Зміна тексту кнопок
    'МЮЗИКЛИ': 'Посилання на мюзикли'  # Зміна 2: Зміна тексту кнопок
}

# Function to handle the /start command
def start(update, context):
    try:
        buttons = parse_buttons('https://www.imdb.com/')  # Change URL to your website URL
        keyboard = [[InlineKeyboardButton(text, callback_data=url)] for text, url in buttons]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Here are the buttons:', reply_markup=reply_markup.to_json())  # Зміна 3: Виклик методу to_json
    except Exception as e:
        logger.error("An error occurred: %s", e)

# Function to handle button click
def button_click(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"You clicked the button: {query.data}")

# Function to handle text message "Genres"
def genres(update, context):
    buttons = [[KeyboardButton(genre)] for genre in genres_movies.keys()]
    markup = ReplyKeyboardMarkup(buttons, row_width=2)
    update.message.reply_text("Choose a movie genre:", reply_markup=markup)

# Function to handle text message with chosen genre
def send_chosen_genre(update, context):
    selected_genre = update.message.text
    update.message.reply_text(f"You selected the genre '{selected_genre}'.")

# Create an instance of the Updater class
updater = Updater(token=TOKEN, use_context=True)

# Create a dispatcher
dispatcher = updater.dispatcher

# Add handler for the /start command
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Add handler for button clicks
button_click_handler = CallbackQueryHandler(button_click)
dispatcher.add_handler(button_click_handler)

# Add handler for clicking genre buttons
genres_handler = MessageHandler(Filters.text & (~Filters.command), genres)
dispatcher.add_handler(genres_handler)

# Add handler for sending chosen genre
send_chosen_genre_handler = MessageHandler(Filters.text & (~Filters.command), send_chosen_genre)
dispatcher.add_handler(send_chosen_genre_handler)

# Start the bot
updater.start_polling()
updater.idle()
