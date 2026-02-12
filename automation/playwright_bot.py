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
import time


logging.basicConfig(
    level= logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('automacao.log', encoding='utf-8'),
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
            while True:
                
                escolha = input('Digite o número de de qual ML você quer ir').strip()
                if escolha in ('1','2','3'):
                    logger.info(f'A opção {escolha} foi armazenada com sucesso')
                    return escolha
                print('Opção Invalida, Digite apenas 1, 2 ou 3')
                logger.warning(f'Opção invalida: {escolha}')
        except Exception:
                logger.exception('Erro ao armanezar a opção')
                raise
    def click (self, locator):
        locator.wait_for(state='visible', timeout=40000)
        locator.click()
        
    def fill (self, locator, value):
        locator.wait_for(state='visible', timeout=40000)
        locator.fill(value)
        
    def wait_visible(self, locator):
        locator.wait_for(state='visible', timeout=40000)

    def login(self):
        try:
            logger.info('Iniciando Login')
            
            self.pagina.goto(self.url_site)
            
            self.fill(self.pagina.get_by_role("textbox", name="usuário"), self.login_usuario)
            self.fill(self.pagina.get_by_role("textbox", name="senha"), self.senha_usuario)
            self.click(self.pagina.get_by_role("button", name="Entrar"))
            self.click(self.pagina.get_by_role("button", name="login"))
            self.click(self.pagina.locator(".btn-sidebar-menu"))
            self.click(self.pagina.get_by_role("link", name="Cadastros"))
            self.click(self.pagina.get_by_role("link", name="Anúncios"))
            self.wait_visible(self.pagina.get_by_role("link", name="gerenciar").first)
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
            self.click(self.pagina.get_by_role("button", name="Mais ações")) 
            self.click(self.pagina.get_by_role("link", name="Importar anúncios"))
            self.click(self.pagina.get_by_text("um anúncio específico"))
            self.click(self.pagina.locator("input[name=\"identificadorAnuncio\"]"))
            self.fill(self.pagina.locator("input[name=\"identificadorAnuncio\"]"), MLBs)
            self.click(self.pagina.get_by_role("button", name="Prosseguir"))
            self.click(self.pagina.get_by_role("button", name="Fechar"))
            logger.info('Importação feita com sucesso')
        except Exception:
            logger.exception('Erro ao realizar a importação')
            raise
        
    def relacionar_ml(self, escolha):
        try:
            logger.info(f'Iniciando processo de relacionar ao ml{escolha}')
            self.click(self.pagina.get_by_role("link", name="filtros"))
            self.pagina.locator("#filtroRelacionados").select_option("N")
            self.click(self.pagina.get_by_role("button", name="Aplicar"))
            self.pagina.get_by_role("columnheader").first.click()
            self.click(self.pagina.get_by_role("button", name="Mais ações ").nth(1))
            self.click(self.pagina.get_by_role("link", name="Relacionar anúncios"))
            self.click(self.pagina.get_by_role("button", name="Relacionar"))
            time.sleep(6) 
            self.click(self.pagina.get_by_role("button", name="fechar "))
            logger.info(f'Processo de relacionar feito com sucesso ao ml{escolha}')
        except Exception:
            logger.exception('Erro no processo de relacionar')
            raise
        
    def sua_MLBs(self):
        try:
            logger.info('Iniciando processo de coleta das MLB(s)')
            print('\n-----DIGITE SUA(s) MLBs-----')
            MLBs = input('Digite suas MLB(s)')
            logger.info('MLB(s) coletadas com sucesso')
            return MLBs
        except Exception:
            logger.exception('Erro ao coletar as MLB(s)')
            raise

    def logout(self):
        try:
            logger.info('Iniciando processo de logout')
            self.click(self.pagina.get_by_role("link", name="Menu Usuário"))
            self.click(self.pagina.get_by_role("link", name="Sair"))
            self.wait_visible(self.pagina.get_by_role("textbox", name="usuário"))
            logger.info('Logout realizado com sucesso')
        except Exception:
            logger.exception('Erro ao tentar fazer o logout')
            raise
            
def main(): 
    try:
        logger.info('Iniciando automação')  
        with sync_playwright() as pw: 
            navegador = pw.chromium.launch(headless=False, slow_mo=800)
            contexto = navegador.new_context()

            pagina = contexto.new_page()
            automacao = TinyAutomation(pagina)

            automacao.login()

            escolha = automacao.opcao_do_usuario()
            
            automacao.ir_ao_ml(escolha)
        
            MLBs = automacao.sua_MLBs()
            
            automacao.importar_para_ml(MLBs)
        
            automacao.relacionar_ml(escolha)
        
            automacao.logout()

            navegador.close()
            logger.info('Automação finalizada com sucesso')
    except Exception:
        logger.exception('Erro em na automação')
if __name__ == '__main__':
    main()


