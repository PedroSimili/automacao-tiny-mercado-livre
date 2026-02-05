'''
Automação de Gerenciamento de Anúncios no Tiny ERP.

Este script utiliza Playwright para automatizar o login no sistema Tiny, 
navegar até a seção de anúncios e acessar a conta do Mercado Livre 
escolhida pelo usuário.

'''


import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import time



load_dotenv()


def tempo_de_espera():
    time.sleep(4)
    

def opcao_do_usuario():
     print('\n-----MENU DE ESCOLHA-----')
     print('1. Mercado Livre 1')
     print('2. Mercado Livre 2')
     print('3. Mercado Livre 3')
     escolha = input('Digite o número de de qual ML você quer ir')
     return escolha
    
escolha = opcao_do_usuario() 

    

with sync_playwright() as pw: 
    navegador = pw.chromium.launch(headless=False)
    contexto = navegador.new_context()
    
    pagina = contexto.new_page()

    url_site = os.getenv('url_site')
    login_usuario = os.getenv('login')
    senha_usuario = os.getenv('senha')
    
    pagina.goto(url_site)
    
    pagina.get_by_role("textbox", name="usuário").fill(login_usuario)
    tempo_de_espera()
    pagina.get_by_role("textbox", name="senha").fill(senha_usuario)
    tempo_de_espera()
    pagina.get_by_role("button", name="Entrar").click()
    tempo_de_espera()
    pagina.get_by_role("button", name="login").click()
    pagina.locator(".btn-sidebar-menu").click()
    pagina.get_by_role("link", name="Cadastros").click()
    pagina.get_by_role("link", name="Anúncios").click()
    time.sleep(6)
    
    try:
        
        print(f'Voce escolheu a opcao {escolha}, vamos abrir o mercado livre {escolha}')
        
        if escolha == '1':
            pagina.get_by_role("link", name="gerenciar").first.click()
        elif escolha == '2':
            pagina.get_by_role("link", name="gerenciar").nth(1).click()
        elif escolha == '3':
            pagina.get_by_role("link", name="gerenciar").nth(2).click()
        print('deu certo')
    except Exception as e:
        print(f'ERRO: {e}')
    

        


    tempo_de_espera()
    time.sleep(10)
    navegador.close()
    