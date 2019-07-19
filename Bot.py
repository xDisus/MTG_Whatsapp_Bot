
# coding: utf-8

# In[1]:


import re
import time
import os
from selenium import webdriver
import requests
from selenium.webdriver.common.keys import Keys
import pyperclip
import itertools


print('Chrome: starting')
#Setamos o caminho de nossa aplicação.
dir_path = os.getcwd()
#Setamos onde está nosso chromedriver.
chrome = dir_path+'\chromedriver.exe'
#Configuramos um profile no chrome para não precisar logar no whats toda vez que iniciar o bot.
options = webdriver.ChromeOptions()
options.add_argument(r"user-data-dir="+dir_path+"\profile\wpp")
options.add_argument("--headless")  
#Iniciamos o driver.
driver = webdriver.Chrome(chrome, options=options)


driver.get('https://web.whatsapp.com/')
driver.implicitly_wait(10)

#caixa_de_pesquisa = driver.find_element_by_class_name('_2zCfw')
print('Chrome: ok')


def mensagem():


    #Setamos a caixa de mensagem.
    caixa_de_mensagem = driver.find_element_by_class_name('_3u328')
    #Enviamos o comando CTRL V (colar) para adicionar a informação da carta
           
    caixa_de_mensagem.send_keys(Keys.CONTROL, 'v')
            
    time.sleep(1)
    #Setamos o botão de enviar e clicamos para enviar.
    botao_enviar = driver.find_element_by_class_name('_3M-N-')
    botao_enviar.click()
    time.sleep(1)

        
def escuta():
#Vamos setar todos as mensagens no grupo.
    post = driver.find_elements_by_class_name('_1zGQT')
#Vamos pegar o índice da última conversa.
    ultimo = len(post) - 1

#Vamos pegar o  texto da última conversa e retornar.
    try:
        texto = post[ultimo].find_element_by_css_selector('span.selectable-text').text
    except:
        texto = 'nontxt'
    return texto

def gotofim():
    fim = 0
    while fim == 0:
        try:
            driver.find_element_by_class_name('_3KRbU').click()
        except:
            fim = 1
            pass
    time.sleep(2)
    
def mtg(card):
    try:
        carta = card.strip()
        url = 'https://api.magicthegathering.io/v1/cards?name="' + str(carta) + '"'

        response = requests.get(url)
        data = response.json()
        cards = data['cards'][1]
        keys = ['Nome','Mana','Tipo','Texto','Poder','Res']
        value = ['name', 'manaCost', 'type', 'text', 'power', 'toughness']
        dic = dict(zip(keys, value))

        carta_resposta = ''
        for nomes,valores in dic.items():
            try:
                carta_resposta += '*' + nomes + ':* ' + cards[valores] + '\n'
            except:
                pass

    except:
        carta_resposta = 'Carta não encontrada'

        carta_resposta = str(carta_resposta) #.replace('\n',' - ')
    return carta_resposta    






if __name__ == '__main__':

    ultimo_texto = '' 
    x = 0
    print('Iniciando loop')
    while True:
        time.sleep(1)
        contatos = driver.find_elements_by_class_name('_2WP9Q')

        for i in itertools.cycle(range(len(contatos))):
            if x== 100:
            	print('Loop:'+srt(x))
            	x = 0
            x+=1
            contatos[i].click()
            time.sleep(2)
            gotofim()
            texto = escuta()
            match = re.search("!!(.+?)##", texto,flags=re.IGNORECASE)
            try:
                resp = match.group(1).strip()
            except:
                resp = ''
            if ultimo_texto != texto and resp != '':
                ultimo_texto = texto
                pyperclip.copy('Pesquisando card: *'+resp+'*')
                mensagem()
                try:
                    pyperclip.copy(mtg(resp))
                    mensagem()
                except:
                    mensagem()

    

