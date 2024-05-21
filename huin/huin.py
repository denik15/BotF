import logging
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import requests
from bs4 import BeautifulSoup

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Token of your bot obtained from BotFather
TOKEN = '7147230738:AAFwGcEAEsrjLeJglnF_7ZltO0eha5scN7A'

# Dictionary containing movie genres and their links
genres_movies = {
    'Action💥': 'https://www.imdb.com/search/title/?genres=action',
    'Crime🤐': 'https://www.imdb.com/search/title/?genres=crime',
    'Sport💪': 'https://www.imdb.com/search/title/?genres=sport',
    'War⚠': 'https://www.imdb.com/search/title/?genres=war',
    'Family👪': 'https://www.imdb.com/search/title/?genres=family',
    'Biography🎞': 'https://www.imdb.com/search/title/?genres=biography',
    'Comedy😂': 'https://www.imdb.com/search/title/?genres=comedy',
    'Horror☠⚠': 'https://www.imdb.com/search/title/?genres=horror',
    'Drama💔🌹': 'https://www.imdb.com/search/title/?genres=drama',
    'Sci-Fi📊🤓': 'https://www.imdb.com/search/title/?genres=sci-fi',
    'Fantasy👽': 'https://www.imdb.com/search/title/?genres=fantasy',
    'Mystery🤠': 'https://www.imdb.com/search/title/?genres=mystery',
    'Romance💞': 'https://www.imdb.com/search/title/?genres=romance',
    'Thriller⏱🔪': 'https://www.imdb.com/search/title/?genres=thriller',
    'Musical🎼': 'https://www.imdb.com/search/title/?genres=musical',
}

# Function to handle the /start command
def start(update, context):
    buttons = [[KeyboardButton(genre)] for genre in genres_movies.keys()]
    markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text("Choose a movie genre:", reply_markup=markup)

# Function to handle text message with chosen genre
def send_chosen_genre(update, context):
    selected_genre = update.message.text
    if selected_genre in genres_movies:
        url = genres_movies[selected_genre]
        update.message.reply_text(f"You selected the genre '{selected_genre}'. Here is the link to {selected_genre} movies: {url}")
    else:
        update.message.reply_text("Sorry, I didn't understand that genre. Please choose from the provided options.")

# Create an instance of the Updater class
updater = Updater(token=TOKEN, use_context=True)

# Create a dispatcher
dispatcher = updater.dispatcher

# Add handler for the /start command
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Add handler for sending chosen genre
send_chosen_genre_handler = MessageHandler(Filters.text & (~Filters.command), send_chosen_genre)
dispatcher.add_handler(send_chosen_genre_handler)

# Start the bot
updater.start_polling()
updater.idle()