
# coding: utf-8

# In[1]:


import re
import time
import os
from selenium import webdriver
import requests
from selenium.webdriver.common.keys import Keys
import pyperclip


# In[2]:


#Setamos o caminho de nossa aplicação.
dir_path = os.getcwd()
#Setamos onde está nosso chromedriver.
chrome = dir_path+'\chromedriver.exe'
#Configuramos um profile no chrome para não precisar logar no whats toda vez que iniciar o bot.
options = webdriver.ChromeOptions()
options.add_argument(r"user-data-dir="+dir_path+"\profile\wpp")
#Iniciamos o driver.
driver = webdriver.Chrome(chrome, options=options)


driver.get('https://web.whatsapp.com/')
driver.implicitly_wait(10)

caixa_de_pesquisa = driver.find_element_by_class_name('_2zCfw')


# In[3]:


def mensagem(mensagem):
    nome_contato = 'Nelson da Trabalhação'

    #Selecionamos o elemento da caixa de pesquisa do whats pela classe.

    #Escreveremos o nome do contato na caixa de pesquisa e aguardaremos 2 segundos.


    #Ao usar este método devemos enviar a mensagem de saudação em uma lista.
    frase_inicial = [mensagem]
    #Setamos a caixa de mensagem como o elemento com a classe _2S1VP.
    caixa_de_mensagem = driver.find_element_by_class_name('_3u328')
    #Validamos se a frase inicial é uma lista.
    if type(frase_inicial) == list:
    #Realizamos um for para enviar cada mensagem na lista.
        for frase in frase_inicial:
    #Escrevemos a frase na caixa de mensagem.
            #caixa_de_mensagem.send_keys(frase)
            
            caixa_de_mensagem.send_keys(Keys.CONTROL, 'v')
            
            time.sleep(1)
    #Setamos o botão de enviar e clicamos para enviar.
            botao_enviar = driver.find_element_by_class_name('_3M-N-')
            botao_enviar.click()
            time.sleep(1)
    else:
        False

        
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


# In[ ]:


ultimo_texto = '' 
nome_contato = 'Nelson da Trabalhação'
#nome_contato = 'Renan Clementino'
caixa_de_pesquisa.send_keys(nome_contato)
time.sleep(2)
#Vamos procurar o contato/grupo que está em um span e possui o título igual que buscamos e vamos clicar.   
contato = driver.find_element_by_xpath('//span[@title = "{}"]'.format(nome_contato))
contato.click()

gotofim()

while True:
    time.sleep(1)
    texto = escuta()
    match = re.search("!!(.+?)##", texto,flags=re.IGNORECASE)
    try:
        resp = match.group(1).strip()
    except:
        resp = ''
    if ultimo_texto != texto and resp != '':
        ultimo_texto = texto
        pyperclip.copy('Pesquisando card: *'+resp+'*')
        mensagem('x')
        try:
            pyperclip.copy(mtg(resp))
            mensagem('x')
        except:
            mensagem('Erro')
    
