import time

import telebot
import emoji

from bs4 import BeautifulSoup as beatiful_soup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from telebot import types, apihelper
from telegram import bot

from Sneaker import Sneaker
from database import save_data, get_count_notes, get_table, delete_data

TOKEN = "5196150095:AAFonrIqmkqiR0LWGvBV2aFt3HBywusi2jE"
bot = telebot.TeleBot(TOKEN, parse_mode=None)
apihelper.SESSION_TIME_TO_LIVE = 10 * 60

url_sneakers = "https://sneakernews.com/release-dates/"
url_jordans = "https://sneakernews.com/air-jordan-release-dates/"
url_yeezys = "https://sneakernews.com/adidas-yeezy-release-dates"
url_clothing = "https://vk.com/madeinrusssia"

bd_sneakers_name = 'sneakers_database'
bd_jordans_name = 'jordans_database'
bd_yeezys_name = 'yeezys_database'

start_point = 0
end_point = 10
status_working = False


@bot.message_handler(commands=['start'])
def cmd_start(message):
    global status_working

    bot.reply_to(message, emoji.emojize('Hi, i`m Sneak.:waving_hand: \n'
                                        'If you need help use command \"/help\"'))

    bot.send_message(message.chat.id, f"I have: \n"
                                      f"    {get_count_notes(bd_sneakers_name)} notes about sneakers produced by brands"
                                      f" such as Nike, Adidas, New Balance, Asics and others;\n"
                                      f"    {get_count_notes(bd_jordans_name)} notes about sneakers produced by"
                                      f" Nike Air Jordan;\n"
                                      f"    {get_count_notes(bd_yeezys_name)} notes about sneakers produced by Yeezy.")

    status_working = True
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton(emoji.emojize(':newspaper:Sneakers news'))
    btn3 = types.KeyboardButton(emoji.emojize(':recycling_symbol:Update'))
    markup.add(btn1)
    markup.add(btn3)
    bot.send_message(message.chat.id, emoji.emojize('What do you want to see next?\n'
                                                    ':newspaper:Sneakers news - if you want to see information about '
                                                    'the release of sneakers;\n'
                                                    ':recycling_symbol:Update - if you want to update information'
                                                    ' about the release of new sneakers.'), reply_markup=markup)


@bot.message_handler(commands=['help'])
def com_help(message):
    if status_working:
        bot.send_message(message.chat.id, 'I can run the following commands:\n'
                                          '/start - Start working;\n')


@bot.message_handler(content_types=['text'])
def hadl_text(message):
    global start_point, end_point
    if status_working:
        if message.text.strip() == emoji.emojize(':newspaper:Sneakers news'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Sneakers')
            btn2 = types.KeyboardButton('Jordans')
            btn3 = types.KeyboardButton('Yeezys')
            btn4 = types.KeyboardButton(emoji.emojize(':BACK_arrow:Back'))
            markup.add(btn1)
            markup.add(btn2)
            markup.add(btn3)
            markup.add(btn4)
            bot.send_message(message.chat.id, 'What type of sneakers do you choose?\n'
                                              'Sneakers - Nike, Adidas, New Balance, Asics and others;\n'
                                              'Jordans - Nike Air Jordan;\n'
                                              'Yeezys - Yeezy.', reply_markup=markup)

        elif message.text.strip() == 'Sneakers':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('10 Sneakers')
            btn2 = types.KeyboardButton(emoji.emojize(':BACK_arrow:Back'))
            markup.add(btn1)
            markup.add(btn2)
            bot.send_message(message.chat.id, 'What you want see next?', reply_markup=markup)

        elif message.text.strip() == 'Jordans':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('10 Jordans')
            btn2 = types.KeyboardButton(emoji.emojize(':BACK_arrow:Back'))
            markup.add(btn1)
            markup.add(btn2)
            bot.send_message(message.chat.id, 'What you want see next?', reply_markup=markup)

        elif message.text.strip() == 'Yeezys':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('10 Yeezys')
            btn2 = types.KeyboardButton(emoji.emojize(':BACK_arrow:Back'))
            markup.add(btn1)
            markup.add(btn2)
            bot.send_message(message.chat.id, 'What you want see next?', reply_markup=markup)

        elif message.text.strip() == '10 Sneakers':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Next 10 sneakers')
            btn2 = types.KeyboardButton(emoji.emojize(':BACK_arrow:Back'))
            markup.add(btn1)
            markup.add(btn2)
            start_point = 0
            end_point = 10
            posts_output(start_point, end_point, bd_sneakers_name, message)
            bot.send_message(message.chat.id, 'What you want see next?', reply_markup=markup)

        elif message.text.strip() == 'Next 10 sneakers':
            bot.send_message(message.chat.id, 'Ok, send 10 more sneakers.')
            start_point += 10
            end_point += 10
            posts_output(start_point, end_point, bd_sneakers_name, message)
            bot.send_message(message.chat.id, 'What you want see next?')

        elif message.text.strip() == '10 Jordans':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Next 10 Jordans')
            btn2 = types.KeyboardButton(emoji.emojize(':BACK_arrow:Back'))
            markup.add(btn1)
            markup.add(btn2)
            start_point = 0
            end_point = 10
            posts_output(start_point, end_point, bd_jordans_name, message)
            bot.send_message(message.chat.id, 'What you want see next?', reply_markup=markup)

        elif message.text.strip() == 'Next 10 Jordans':
            bot.send_message(message.chat.id, 'Ok, send 10 more jordans')
            start_point += 10
            end_point += 10
            posts_output(start_point, end_point, bd_jordans_name, message)
            bot.send_message(message.chat.id, 'What you want see next?')

        elif message.text.strip() == '10 Yeezys':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Next 10 Yeezys')
            btn2 = types.KeyboardButton(emoji.emojize(':BACK_arrow:Back'))
            markup.add(btn1)
            markup.add(btn2)
            start_point = 0
            end_point = 10
            posts_output(start_point, end_point, bd_yeezys_name, message)
            bot.send_message(message.chat.id, 'What you want see next?', reply_markup=markup)

        elif message.text.strip() == 'Next 10 Yeezys':
            bot.send_message(message.chat.id, 'Ok, send 10 more yeezys')
            start_point += 10
            end_point += 10
            posts_output(start_point, end_point, bd_yeezys_name, message)
            bot.send_message(message.chat.id, 'What you want see next?')

        elif message.text.strip() == emoji.emojize(':recycling_symbol:Update'):
            source_data_sneakers = ''
            source_data_jordans = ''
            source_data_yeezys = ''

            sneakers_list = list()
            jordans_list = list()
            yeezys_list = list()

            bot.send_message(message.chat.id, " Now I will update information about the releases of "
                                              "new pairs of sneakers.\n"
                                              "Please wait a couple of minutes.")

            try:
                source_data_sneakers = searching_data(url_sneakers, 6)
                bot.send_message(message.chat.id, emoji.emojize("Sneakers successfully opened. :party_popper:"))
                source_data_jordans = searching_data(url_jordans, 4)
                bot.send_message(message.chat.id, emoji.emojize("Nike Air Jordan successfully opened. :party_popper:"))
                source_data_yeezys = searching_data(url_yeezys, 2)
                bot.send_message(message.chat.id, emoji.emojize("Yeezy successfully opened. :party_popper:"))
            except Exception as ex_searching:
                print(ex_searching)
                bot.send_message(message.chat.id, emoji.emojize("An error occurred while opening the source. "
                                                                ":disappointed:\n"
                                                                "Please, try again."))

            try:
                sneakers_list = parser_from_sneaker_news(source_data_sneakers, 6)
                jordans_list = parser_from_sneaker_news(source_data_jordans, 4)
                yeezys_list = parser_from_sneaker_news(source_data_yeezys, 2)

                bot.send_message(message.chat.id, emoji.emojize("Parsing completed successfully. :party_popper:"))
            except Exception as ex_parsing:
                print(ex_parsing)
                bot.send_message(message.chat.id, emoji.emojize("An error occurred during parsing. :disappointed:\n"
                                                                "Please, try again."))

            clear_database()

            try:
                save_data(sneakers_list, bd_sneakers_name)
                save_data(jordans_list, bd_jordans_name)
                save_data(yeezys_list, bd_yeezys_name)

                bot.send_message(message.chat.id, emoji.emojize("Data saved successfully. :party_popper:"))
            except Exception as ex_saving_data:
                print(ex_saving_data)
                bot.send_message(message.chat.id, emoji.emojize("An error occurred during saving data. :disappointed:\n"
                                                                "Please, try again."))

            bot.send_message(message.chat.id, emoji.emojize('Data received successfully! :party_popper:\n'
                                                            'Now you can see the updated information.'))

        elif message.text.strip() == emoji.emojize(':BACK_arrow:Back'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton(emoji.emojize(':newspaper:Sneakers news'))
            btn3 = types.KeyboardButton(emoji.emojize(':recycling_symbol:Update'))

            markup.add(btn1)
            markup.add(btn3)

            bot.send_message(message.chat.id, 'You are back to the main menu.', reply_markup=markup)


def parser_from_sneaker_news(r, length):
    sneakers = list()
    soup = beatiful_soup(r, "html.parser")
    try:
        for i in range(1, length):
            sneakers_html = soup.find_all('div', class_='releases-box col lg-2 sm-6 paged-' + str(i))

            for item in sneakers_html:
                sneaker = Sneaker()

                sneaker.image = item.find('img')['src']
                sneaker.name = item.find('h2').get_text().replace("'", '').replace('"', '')[1:-1]
                sneaker.drop_date = item.find('span', class_='release-date').get_text().replace(' ', '')

                try:
                    where_buy_box = item.find('div', class_="sn_where_buy_box")
                    sneaker.link = where_buy_box.find('a')['href']
                except Exception as ex:
                    print(ex)
                    sneaker.link = "No Info"
                sneaker.price_usd = (item.find('span', class_='release-price').get_text()[2:])

                try:
                    sneaker.price_rub = int(sneaker.price_usd) * 100  # сделать нормальный парсинг курса
                except Exception as ex:
                    sneaker.price_rub = 'N/A'
                    print(ex)

                sneaker_post_data_html = item.find('div', class_='post-data')
                sneaker_post_data = sneaker_post_data_html.find_all('p')

                sneaker.size = string_format(sneaker_post_data[0].get_text())
                sneaker.color = string_format(sneaker_post_data[1].get_text())
                sneaker.style_code = string_format(sneaker_post_data[2].get_text())
                sneaker.regions = sneaker_post_data[3].get_text().replace('  ', '').replace("'", '').replace('"', '')[
                                  sneaker_post_data[3].get_text().find(':') + 1:]

                sneaker.show_info()
                sneakers.append(sneaker)
    except Exception as ex:
        print(ex)
    finally:
        return sneakers


def clear_database():
    delete_data(bd_sneakers_name)
    delete_data(bd_jordans_name)
    delete_data(bd_yeezys_name)


def scrolling_page(browser, length):
    for i in range(1, length):
        time.sleep(6)
        btn = browser.find_element(By.ID, 'sneaker-release-load-more-btn')
        btn.click()


def searching_data(url, length):
    options = Options()
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    browser.fullscreen_window()
    browser.get(url)
    time.sleep(10)

    if len(browser.find_elements(By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')) > 0:
        btn = browser.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
        btn.click()

    scrolling_page(browser, length)
    source_data = browser.page_source
    return source_data


def posts_output(start_point, end_point, name, message):
    table = get_table(start_point, end_point, name)
    count = 0
    for raws in table:
        try:
            count += 1
            description = f"Drop date: {raws['date']}\n" \
                          f"{raws['name']}\n" \
                          f"For {raws['size']}\n" \
                          f"Price: {raws['price_usd']}$ \\ {raws['price_rub']}₽\n" \
                          f"Color: {raws['color']}\n" \
                          f"Code {raws['style_code']}\n" \
                          f"Available for: {raws['regions']}\n" \
                          f"Where to buy: {raws['link']}"
            bot.send_photo(message.chat.id, raws['image'], description)
        except Exception as ex:
            bot.send_message(message.chat.id, "Error")
            print(ex)
        time.sleep(0.5)
    if count == 0:
        bot.send_message(message.chat.id, 'Sorry, i have no more posts')


def string_format(string):
    string = string.replace('  ', '').replace("'", '').replace('"', '')[1:]
    if string.count(':') > 0:
        string = string[string.find(':') + 1:]
    return string


bot.polling(none_stop=True, interval=0)
