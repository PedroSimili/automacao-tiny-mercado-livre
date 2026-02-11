'''
Automação de Gerenciamento de Anúncios no Tiny ERP.

Este script utiliza Playwright para automatizar o login no sistema Tiny, 
navegar até a seção de anúncios e acessar a conta do Mercado Livre 
escolhida pelo usuário.

'''


import os
from dotenv import load_dotenv
import logging
from playwright.sync_api import sync_playwright


logging.basicConfig(
    level= logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('automacai.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

class TinyAutomation:
    def __init__(self, pagina):
        self.pagina = pagina
        self.url_site = os.getenv('url_site')
        self.login_usuario = os.getenv('login')
        self.senha_usuario = os.getenv('senha')
        

    def opcao_do_usuario(self):
        try:
            logger.info('Inciando programa')
            print('\n-----MENU DE ESCOLHA-----')
            print('1. Mercado Livre 1')
            print('2. Mercado Livre 2')
            print('3. Mercado Livre 3')
            escolha = input('Digite o número de de qual ML você quer ir')
            return escolha

            logger.info('Opção armazenada com sucesso')
        except Exception:
            logger.exception('Erro ao armanezar a opção')
            raise

    def login(self):
        try:
            logger.info('Iniciando Login')
            
            self.pagina.goto(self.url_site)
            self.pagina.get_by_role("textbox", name="usuário").wait_for(state='visible', timeout=10000)
            self.pagina.get_by_role("textbox", name="usuário").fill(self.login_usuario)
            self.pagina.get_by_role("textbox", name="senha").wait_for(state='visible', timeout = 10000)
            self.pagina.get_by_role("textbox", name="senha").fill(self.senha_usuario)
            self.pagina.get_by_role("button", name="Entrar").wait_for(state='visible', timeout = 10000)
            self.pagina.get_by_role("button", name="Entrar").click()
            self.pagina.get_by_role("button", name="login").wait_for(state='visible', timeout=10000)
            self.pagina.get_by_role("button", name="login").click()
            self.pagina.locator(".btn-sidebar-menu").wait_for(state='visible', timeout=10000)
            self.pagina.locator(".btn-sidebar-menu").click()
            self.pagina.get_by_role("link", name="Cadastros").wait_for(state='visible', timeout=10000)
            self.pagina.get_by_role("link", name="Cadastros").click()
            self.pagina.get_by_role("link", name="Anúncios").wait_for(state='visible', timeout=10000)
            self.pagina.get_by_role("link", name="Anúncios").click()
            self.pagina.get_by_role("link", name="gerenciar").first.wait_for(state='visible', timeout=10000)
            logger.info('Login feito com sucesso!!!')
        except Exception:
            logger.exception('Erro no Login')
            raise

    def ir_ao_ml(self, escolha):
        try:
            logger.info(f'Indo para o ML{escolha}')
            print(f'Voce escolheu a opcao {escolha}, vamos abrir o mercado livre {escolha}')
            
            if escolha == '1':
                self.pagina.get_by_role("link", name="gerenciar").first.click()
            elif escolha == '2':
                self.pagina.get_by_role("link", name="gerenciar").nth(1).click()
            elif escolha == '3':
                self.pagina.get_by_role("link", name="gerenciar").nth(2).click()
            logger.info(f'opção ML{escolha} feita com sucesso')
        except Exception:
            logger.exception('Erro ao tentar ir ao ML')
            raise
            
    def importar_para_ml(self, MLBs):
        try:
            logger.info('Inciando processo de importação...')
            self.pagina.get_by_role("button", name="Mais ações").wait_for(state='visible', timeout=10000)
            self.pagina.get_by_role("button", name="Mais ações").click()   
            self.pagina.get_by_role("link", name="Importar anúncios").wait_for(state='visible', timeout=10000)
            self.pagina.get_by_role("link", name="Importar anúncios").click()
            self.pagina.get_by_text("um anúncio específico").wait_for(state='visible', timeout=10000)
            self.pagina.get_by_text("um anúncio específico").click()
            self.pagina.locator("input[name=\"identificadorAnuncio\"]").wait_for(state='visible', timeout=10000)
            self.pagina.locator("input[name=\"identificadorAnuncio\"]").click()
            self.pagina.locator("input[name=\"identificadorAnuncio\"]").fill(MLBs)
            self.pagina.get_by_role("button", name="Prosseguir").wait_for(state='visible', timeout=10000)
            self.pagina.get_by_role("button", name="Prosseguir").click()
            #self.tempo_de_espera()
            self.pagina.get_by_role("button", name="Fechar").wait_for(state='visible', timeout=10000)
            self.pagina.get_by_role("button", name="Fechar").click()
            logger.info('Importação feita com sucesso')
        except Exception:
            logger.exception('Erro ao realizar a importação')
            raise
        
    def relacionar_ml(self, escolha):
        try:
            logger.info(f'Iniciando processo de relacionar ao ml{escolha}')
            self.pagina.get_by_role("link", name="filtros").wait_for(state='visible', timeout=10000)
            self.pagina.get_by_role("link", name="filtros").click()
            self.pagina.locator("#filtroRelacionados").select_option("N")
            self.pagina.get_by_role("button", name="Aplicar").wait_for(state='visible', timeout=10000)
            self.pagina.get_by_role("button", name="Aplicar").click()
            self.pagina.get_by_role("columnheader").first.click()
            self.pagina.get_by_role("button", name="Mais ações").wait_for(state='visible', timeout=10000)
            self.pagina.get_by_role("button", name="Mais ações").nth(1).click()
            self.pagina.get_by_role("link", name="Relacionar anúncios").wait_for(state='visible', timeout=10000)
            self.pagina.get_by_role("link", name="Relacionar anúncios").click()
            self.pagina.get_by_role("button", name="Relacionar").click()
            self.pagina.get_by_role("button", name="fechar ").wait_for(state='visible', timeout=10000)
            self.pagina.get_by_role("button", name="fechar ").click()
            logger.info(f'Processo de relacionar feito com sucesso ao ml{escolha}')
        except Exception:
            logger.exception('Erro no processo de relacionar')
            raise
        
    def Sua_MLBs(self):
        try:
            logger.info('Iniciando processo de coleta das MLB(s)')
            print('\n-----DIGITE SUA(s) MLBs-----')
            MLBs = input('Digite suas MLB(s)')
            return MLBs
            logger.info('MLB(s) coletadas com sucesso')
        except Exception:
            logger.exception('Erro ao coletar as MLB(s)')
            raise

    def logout(self):
        try:
            logger.info('Iniciando processo de logout')
            self.pagina.get_by_role("link", name="Menu Usuário").wait_for(state='visible', timeout=10000)
            self.pagina.get_by_role("link", name="Menu Usuário").click()
            self.pagina.get_by_role("link", name="Sair").wait_for(state='visible', timeout=10000)
            self.pagina.get_by_role("link", name="Sair").click()
            self.pagina.get_by_role("textbox", name="usuário").wait_for(state='visible', timeout=10000)
            logger.info('Logout realizado com sucesso')
        except Exception:
            logger.exception('Erro ao tentar fazer o logout')
            raise
            
def main(): 
    try:
        logger.info('Iniciando automação')  
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
        
            automacao.relacionar_ml(escolha)
        
            automacao.logout()

            navegador.close()
            logger.info('Automação finalizada com sucesso')
    except Exception:
        logger.exception('Erro em na automação')
if __name__ == '__main__':
    main()


