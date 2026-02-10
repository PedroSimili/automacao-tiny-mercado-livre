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

class TinyAutomation:
    def __init__(self, pagina):
        self.pagina = pagina
        self.url_site = os.getenv('url_site')
        self.login_usuario = os.getenv('login')
        self.senha_usuario = os.getenv('senha')

    def tempo_de_espera(self, segundos=3):
        time.sleep(segundos)
        

    def opcao_do_usuario(self):
        print('\n-----MENU DE ESCOLHA-----')
        print('1. Mercado Livre 1')
        print('2. Mercado Livre 2')
        print('3. Mercado Livre 3')
        escolha = input('Digite o número de de qual ML você quer ir')
        return escolha
    #escolha = opcao_do_usuario()

    def login(self):
        self.pagina.goto(self.url_site)
        
        self.pagina.get_by_role("textbox", name="usuário").fill(self.login_usuario)
        self.tempo_de_espera()
        self.pagina.get_by_role("textbox", name="senha").fill(self.senha_usuario)
        self.tempo_de_espera()
        self.pagina.get_by_role("button", name="Entrar").click()
        self.tempo_de_espera()
        self.pagina.get_by_role("button", name="login").click()
        self.pagina.locator(".btn-sidebar-menu").click()
        self.pagina.get_by_role("link", name="Cadastros").click()
        self.pagina.get_by_role("link", name="Anúncios").click()
        time.sleep(6)

    def ir_ao_ml(self, escolha):
        try:
            print(f'Voce escolheu a opcao {escolha}, vamos abrir o mercado livre {escolha}')
            
            if escolha == '1':
                self.pagina.get_by_role("link", name="gerenciar").first.click()
            elif escolha == '2':
                self.pagina.get_by_role("link", name="gerenciar").nth(1).click()
            elif escolha == '3':
                self.pagina.get_by_role("link", name="gerenciar").nth(2).click()
            print('deu certo')
        except Exception as e:
            print(f'ERRO: {e}')
            
    def importar_para_ml(self, MLBs):
        self.pagina.get_by_role("button", name="Mais ações").click()   
        self.pagina.get_by_role("link", name="Importar anúncios").click()
        self.pagina.get_by_text("um anúncio específico").click()
        self.pagina.locator("input[name=\"identificadorAnuncio\"]").click()
        self.pagina.locator("input[name=\"identificadorAnuncio\"]").fill(MLBs)
        self.pagina.get_by_role("button", name="Prosseguir").click()
        self.tempo_de_espera()
        self.pagina.get_by_role("button", name="Fechar").click()
        
    def relacionar_ml(self):
        self.pagina.get_by_role("link", name="filtros").click()
        self.tempo_de_espera()
        self.pagina.locator("#filtroRelacionados").select_option("N")
        self.pagina.get_by_role("button", name="Aplicar").click()
        self.tempo_de_espera()
        self.pagina.get_by_role("columnheader").first.click()
        self.tempo_de_espera()
        self.pagina.get_by_role("button", name="Mais ações").nth(1).click()
        self.pagina.get_by_role("link", name="Relacionar anúncios").click()
        self.pagina.get_by_role("button", name="Relacionar").click()
        self.tempo_de_espera()
        #self.pagina.get_by_role("button", name="Fechar", exact=True).click()
        self.pagina.get_by_role("button", name="fechar ").click()
        
    def Sua_MLBs(self):
        print('\n-----DIGITE SUA(s) MLBs-----')
        MLBs = input('Digite suas MLB(s)')
        return MLBs
    #MLBs = Sua_MLBs()

    def logout(self):
        self.pagina.get_by_role("link", name="Menu Usuário").click()
        self.tempo_de_espera()
        self.pagina.get_by_role("link", name="Sair").click()
        self.tempo_de_espera()
        
    
    
def main():    
    with sync_playwright() as pw: 
        navegador = pw.chromium.launch(headless=False)
        contexto = navegador.new_context()

        pagina = contexto.new_page()
        automacao = TinyAutomation(pagina)

        automacao.login()

        escolha = automacao.opcao_do_usuario()
         
        automacao.ir_ao_ml(escolha)
    
        MLBs = automacao.Sua_MLBs()
        
        automacao.importar_para_ml(MLBs)
    
        automacao.relacionar_ml()
    
        automacao.logout()

        navegador.close()
if __name__ == '__main__':
    main()
