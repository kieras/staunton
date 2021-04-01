from lxml import html
import datetime
import json
import os
import pytz
import requests
import textwrap
import time

url_chat_webhook = 'https://chat.googleapis.com/v1/spaces/AAAALKak-Us/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=4SRdfiEDQgPB2S1rrC6SozQ96UG7XrV3NarKDzj3Z8I%3D'

url_cust_id = 'https://lista.mercadolivre.com.br/_CustId_70565267'

urls = ['https://produto.mercadolivre.com.br/MLB-1600460311',
        'https://produto.mercadolivre.com.br/MLB-1601403125',
        'https://produto.mercadolivre.com.br/MLB-1436130428',
        'https://produto.mercadolivre.com.br/MLB-1619225228',
        'https://produto.mercadolivre.com.br/MLB-1806750212']

expected_title = ['Peças De Xadrez Germam Staunton + Damas Extras 10 Cm',
                  'Peças De Xadrez Rei 10 Cm + Damas Extras German Staunton',
                  'Peças De Xadrez Germam Staunton Damas Extras Rei 10 Cm',
                  'Peças De Xadrez Stauton Damas Extras Rei 10 Cm Chumbadas',
                  'Peças De Xadrez Rei 10 Cm German Staunton Madeira Jacaranda']
expected_price = ['4.500',
                  '5.000',
                  '4.500',
                  '4.500',
                  '4.500']
expected_description = ['Peças de xadrez réplica German Staunton%Mais uma reprodução do jogo de xadrez famoso em torneios mundiais. Este conjunto contém 34 peças (damas extras) com rei medindo 10 cm de altura e 4 cm de base. As peças são chumbadas com puro chumbo (cerca de 1,6 kg) dando mais estabilidade ao jogar Blitz. As peças são protegidas por feltro em suas bases para melhor deslisamento na superfície. As peças tem um acabamento em verniz marítimo gloss extra brilhante natural , para realçar melhor a beleza da madeira.%Peças de xadrez em madeira nobre jacaranda do cerrado e madeira pau-marfim nobre',
                        'Peças de xadrez réplica German Staunton%Mais uma reprodução do jogo de xadrez famoso em torneios mundiais. Este conjunto contém 34 peças (damas extras) com rei medindo 10 cm de altura e 4 cm de base. As peças são chumbadas com puro chumbo (cerca de 1,6 kg) dando mais estabilidade ao jogar Blitz. As peças são protegidas por feltro em suas bases para melhor deslisamento na superfície. As peças tem um acabamento em verniz marítimo gloss extra brilhante natural , para realçar melhor a beleza da madeira.%Peças de xadrez em madeira nobre jacaranda do cerrado e madeira pau-marfim nobre',
                        'Mais uma reprodução do jogo de xadrez famoso em torneios mundiais. Este conjunto contém 34 peças (damas extras) com rei medindo 10 cm de altura e 4 cm de base. As peças são chumbadas com puro chumbo (cerca de 1,6 kg) dando mais estabilidade ao jogar Blitz. As peças são protegidas por feltro em suas bases para melhor deslisamento na superfície. As peças tem um acabamento em verniz marítimo gloss extra brilhante natural , para realçar melhor a beleza da madeira.%Peças de xadrez em madeira nobre jacaranda do cerrado e madeira pau-marfim nobre%TABULEIRO NÃO ACOMPANHA AS PECAS ! %VENDIDO SEPARADO POR 500,00 OU COMPLETO COM PECAS POR 950,00%O VALOR DE 450,00 É APENAS DAS PEÇAS CHUMBADAS COM 34 PEÇAS , COM FELTRO , MODELO FIDE GERMAM DAS FOTOS 1 E 2',
                        'Mais uma reprodução do jogo de xadrez famoso em torneios mundiais. Este conjunto contém 34 peças (damas extras) com rei medindo 10 cm de altura e 4 cm de base. As peças são chumbadas com puro chumbo (cerca de 1,6 kg) dando mais estabilidade ao jogar Blitz. As peças são protegidas por feltro em suas bases para melhor deslisamento na superfície. As peças tem um acabamento em verniz marítimo gloss extra brilhante natural , para realçar melhor a beleza da madeira.%Peças de xadrez em madeira nobre massaranduba negra ou braúna e madeira pau-marfim nobre%A cor preta das peças são cores naturais da madeira , NÃO uso tintas',
                        'Peças de xadrez German Staunton em madeira Jacaranda caviuna e paumarfim , com damas extras , chumbadas, com feltro e acabamento em verniz PU automotivo.%Rei 10 cm por 3,9 cm de base%Fabricado uma a uma %Fabricado no Brasil 100% nacional, com madeiras nobres/raras']
expected_last_question = ['',
                          '',
                          '',
                          '',
                          '']
expected_last_response = ['',
                          '',
                          '',
                          '',
                          '']

sleep_seconds = 6
truncate_description_width = 80

xpath_title = '//*[@id="root-app"]/div/div[3]/div/div[2]/div[1]/div/div[1]/div/div[2]/h1'
xpath_price = '//*[@id="root-app"]/div/div[3]/div/div[2]/div[1]/div/div[2]/div/div[1]/div/span/span[2]'
xpath_description = '//*[@id="root-app"]/div/div[3]/div/div[1]/div[2]/div[3]/div/p'
xpath_last_question = '//*[@id="questions"]/div[1]/div[1]/div/div[1]/div/span'
xpath_last_response = '//*[@id="questions"]/div[1]/div[1]/div/div[1]/div[2]/div/div/span'

def main():
    hour_beat = -1
    while True:
        try:
            update()
            print('********************** Waiting... ***********************')

            # do less requests at night...
            mytime = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))

            if hour_beat == -1:
                hour_beat = mytime.hour

            if mytime.hour < 5 or mytime.hour > 23:
                print("It's night. Wait more...")
                time.sleep(sleep_seconds*10)
                hour_beat = mytime.hour
            else:
                if hour_beat < mytime.hour:
                    print("Sending heartbeat for hour " + str(mytime.hour))
                    notify(url_cust_id, "Heartbeat", "Heartbeat for hour " + str(mytime.hour))
                    hour_beat = mytime.hour

                time.sleep(sleep_seconds)
        except Exception as e:
            print('An exception occured: ' + str(e))
            try:
                notify(url_cust_id,
                    'Staunton exception!', 'An exception occured: ' + str(e))
            except Exception as e2:
                print('Error sending exception notification.' + str(e2))
            time.sleep(sleep_seconds)

def update():
    index_ad = 0
    print(str(datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))))
    for url in urls:
        r = requests.get(url)

        if r.status_code != 200:
            print('Error: ' + str(r.status_code))
            notify(url_cust_id, 'Request error',
                   'Error: ' + str(r.status_code))

        tree = html.fromstring(r.content)
        try:
            title = tree.xpath(xpath_title + '/text()')[0]
            price = tree.xpath(xpath_price + '/text()')[0]
            description_array = tree.xpath(xpath_description + '/text()')
            description = "%".join(description_array)
            last_question_array = tree.xpath(xpath_last_question + '/text()')
            last_question = "%".join(last_question_array)
            last_response_array = tree.xpath(xpath_last_response + '/text()')
            last_response = "%".join(last_response_array)
        except:
            title = ''
            price = ''
            description = ''
            last_question = ''
            last_response = ''


        report(url, index_ad, title, price, description, last_question, last_response)
        index_ad = index_ad + 1


def report(url, index_ad, title, price, description, last_question, last_response):
    print('[' + str(index_ad) + ']: ' + url)

    if title == '' or price == '' or description == '' or last_question == '' or last_response == '':
        print('Empty values. Skipping...')
        return

    has_changed = False
    if title != expected_title[index_ad]:
        has_changed = True
        print('Title changed! New value: ' + title)
        notify(url, 'Title changed!', 'New value: ' + title)
        expected_title[index_ad] = title

    if price != expected_price[index_ad]:
        has_changed = True
        print('Price changed! New value: ' + price)
        notify(url, 'Price changed!', 'New value: ' + price)

    if description != expected_description[index_ad]:
        has_changed = True
        print('Description changed! New value: ' + description)
        notify(url, 'Description changed!', 'New value: ' + description)
        expected_description[index_ad] = description

    if last_question != expected_last_question[index_ad]:
        has_changed = True
        print('Last question changed! New value: ' + last_question)
        notify(url, 'Last question changed!', 'New value: ' + last_question)
        expected_last_question[index_ad] = last_question

    if last_response != expected_last_response[index_ad]:
        has_changed = True
        print('Last response changed! New value: ' + last_response)
        notify(url, 'Last response changed!', 'New value: ' + last_response)
        expected_last_response[index_ad] = last_response

    if not has_changed:
        print('Nothing changed.')
    else:
        print()
        print('--------------------------')
        print('Original values:')
        print(title)
        print(price)
        print(textwrap.shorten(description, width=truncate_description_width))
        print(last_question)
        print(last_response)


def notify(url, title, text):
    # try:
    #     os.system("""
    #             osascript -e 'display notification "{}" with title "{}"'
    #             """.format(text + '' + url, title))
    # except:
    #     print("Error notifying MacOS")

    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    text = '`{}` *{}* <{}|{}!>'.format(title, text, url, url)

    chat_response_payload_json = {
        'text': text
    }

    chat_response_payload = json.dumps(chat_response_payload_json, indent=2)

    response = requests.post(
        url_chat_webhook, data=chat_response_payload, headers=message_headers)


if __name__ == '__main__':
    main()
