from telebot import TeleBot,types
import requests
from bs4 import BeautifulSoup
import urllib

bot = TeleBot("1496165926:AAF7_6NjW93He6D01uSAFIFy4zgLxn9dEzw")

def fetch_trends():
    url = "https://bubbletrends.herokuapp.com/trends"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    trends = " "
    for i in soup.find_all('tr'):
        pdt_name = i.find_all('td')[1].get_text()
        no_of_results = i.find_all('td')[2].get_text()
        trends= trends + f"{pdt_name} {no_of_results}\n"
    return trends

def fetch_filtered_trends(number):
    url = "https://bubbletrends.herokuapp.com/trends"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    trends = " "
    for i in soup.find_all('tr'):
        pdt_name = i.find_all('td')[1].get_text()
        no_of_results_w = i.find_all('td')[2].get_text()
        no_of_results = i.find_all('td')[2].get_text().split(" ")[0]
        converted = no_of_results.split(",")
        simple = ""
        for i in converted:
            simple = simple + i
        print(simple)
        converted = int(simple)
        print(converted)
        if converted < number:
            trends= trends + f"{pdt_name} {no_of_results_w}\n"
    return trends    

def get_article():
    resp = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    article_name = resp.url.split("/")[-1]
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{article_name}"
    return requests.get(url).json()

@bot.message_handler(commands=["trends"])
def send_bubble_trends(message):
    trends = fetch_trends()
    bot.send_message(message.chat.id,trends)

@bot.message_handler(commands=["1ktrends"])
def send_1kbubble_trends(message):
    trends = fetch_filtered_trends(1000)
    bot.send_message(message.chat.id,trends)

@bot.message_handler(commands=["lesstrends"])
def send_500bubble_trends(message):
    trends = fetch_filtered_trends(500)
    bot.send_message(message.chat.id,trends)    


@bot.message_handler(commands=["random"])
def send_random_article(message):
    """/random."""
    article = get_article()
    msg_content = "<b>{0}</b> <a href='{1}'>&#8204;</a>\n{2}".format(
        article["title"],
        article.get("thumbnail", {}).get("source", ""),
        article["extract"],
    )
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    markup.add("Read-Wiki", "Skip")
    msg = bot.send_message(
        message.chat.id, msg_content, reply_markup=markup, parse_mode="html",
    )
    bot.register_next_step_handler(msg, send_article_url, article["content_urls"])


def send_article_url(message, article_urls):
    if message.text == "Read-Wiki":
        bot.send_message(message.chat.id, article_urls["desktop"]["page"])


@bot.message_handler(commands=["start", "help"])
def send_instructions(message):
    """/start, /help"""
    msg_content = (
        "*Available commands:*\n\n" "/random - get summary of random Wikipedia article\n /trends to get redbubble latest trends\n /1ktrends to get 1k less trends \n /lesstrends to get 1k less trends"
    )
    bot.send_message(
        message.chat.id, msg_content, parse_mode="markdown",
    )


bot.polling(none_stop=True)