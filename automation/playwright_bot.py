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
import re
from datetime import datetime


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
        
        self.tempo_inicio = None
        self.tempo_fim = None
        self.escolha_ml = None
        self.mlbs = []
        self.mlbs_sucesso = []
        self.mlbs_falha = []
        
    def print_sumarry(self):
        self.tempo_fim = time.time()
        tempo_total = (
            self.tempo_fim - self.tempo_inicio
            if self.tempo_fim and self.tempo_inicio else 0
        )
        
        total = len(self.mlbs)
        sucesso = len(self.mlbs_sucesso)
        falha = len(self.mlbs_falha)
        
        pct_sucesso = (sucesso / total * 100) if total else 0
        pct_falha = (falha / total * 100) if total else 0
        
        logger.info('-----RESUMO DA OPERAÇÃO-----')
        logger.info(f'Conta ML escolhida: {self.escolha_ml}')
        logger.info(f'Tempo total: {tempo_total:.2f}s ({tempo_total/60:.2f} minutos)')
        
        logger.info('-----ESTATÍSTICAS-----')
        logger.info(f' Total de MLB(s): {total}')
        logger.info(f' MLB(s) bem sucedidas: {sucesso} ({pct_sucesso:.1f}%)')
        logger.info(f' MLB(s) com erro: {falha} ({pct_falha:.1f}%)')
        
        if self.mlbs_sucesso:
            logger.info('MLB(s) IMPORTADAS COM SUCESSO: ')
            for mlb in self.mlbs_sucesso:
                logger.info(f' {mlb}')
                
        if self.mlbs_falha:
            logger.info('MLB(s) COM FALHA: ')
            for mlb in self.mlbs_falha:
                logger.info(f' {mlb}')
                
        if falha == 0 and total > 0:
            logger.info('AUTOMAÇÃO CONCLUIDA COM SUCESSO')
        elif sucesso == 0 and total > 0:
            logger.error('AUTOMAÇÃO FALHOU - NENHUMA MLB(s) FOI IMPORTADA')
        else:
            logger.warning('AUTOMAÇÃO CONCLUIDA COM ALGUMSA FALHAS')
        
        logger.info(f"Finalizada às {datetime.now().strftime('%H:%M:%S')}")
        
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
            
            try:
                botao_login = self.pagina.get_by_role("button", name="login")
                botao_login.wait_for(state='visible', timeout=3000)
                botao_login.click()
            except Exception:
                logger.info('Botão login não apareceu, seguindo fluxo')
                
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
            
    def importar_para_ml(self, mlb):
        try:
            logger.info('Inciando processo de importação...')
            self.click(self.pagina.get_by_role("button", name="Mais ações")) 
            self.click(self.pagina.get_by_role("link", name="Importar anúncios"))
            self.click(self.pagina.get_by_text("um anúncio específico"))
            self.click(self.pagina.locator("input[name=\"identificadorAnuncio\"]"))
            self.fill(self.pagina.locator("input[name=\"identificadorAnuncio\"]"), mlb)
            self.click(self.pagina.get_by_role("button", name="Prosseguir"))
            erro_importacao = self.pagina.get_by_text(
                re.compile(
                    r"Erro\s*Erro ao buscar a fam[ií]lia|Erro ao buscar a fam[ií]lia|n[aã]o foi encontrad[ao] individualmente",
                    re.IGNORECASE
                )
            ).first
            titulo_erro = self.pagina.get_by_role(
                "heading",
                name=re.compile(r"^Erro$", re.IGNORECASE)
            ).first
            houve_erro_importacao = False
            mensagem_erro = ''

            try:
                erro_importacao.wait_for(state='visible', timeout=12000)
                houve_erro_importacao = True
                mensagem_erro = erro_importacao.inner_text().strip()
            except Exception:
                try:
                    titulo_erro.wait_for(state='visible', timeout=1500)
                    houve_erro_importacao = True
                    mensagem_erro = 'Erro exibido na tela de importação'
                except Exception:
                    houve_erro_importacao = False

            if houve_erro_importacao:
                logger.error(f'Erro na importação da MLB {mlb}: {mensagem_erro}')
                self.click(self.pagina.get_by_role("button", name="Fechar"))
                raise RuntimeError(f'Falha na importação da MLB {mlb}')
            self.click(self.pagina.get_by_role("button", name="Fechar"))
            logger.info(f'Importação feita com sucesso para {mlb}')
        except Exception:
            logger.exception('Erro ao realizar a importação')
            raise

    def solicitar_mlb_correcao(self, mlb_com_erro):
        while True:
            nova_mlb = input(
                f'Erro ao importar {mlb_com_erro}. Digite uma MLB correta para nova tentativa: '
            ).strip().upper()

            if re.fullmatch(r'MLB\d+', nova_mlb):
                logger.info(f'Nova MLB informada para correção: {nova_mlb}')
                return nova_mlb

            print('MLB inválida. Use o formato MLB123456.')
            logger.warning(f'MLB de correção inválida: {nova_mlb}')

    def importar_novamente(self, mlb, max_tentativas = 2, esperar_segundos = 2):
        mlb_tentativa = mlb
        for tentativa in range(1, max_tentativas + 1):
            try:
                logger.info(
                    f'Importando {mlb_tentativa} (tentativa {tentativa}/{max_tentativas})'
                )
                self.importar_para_ml(mlb_tentativa)
                self.mlbs_sucesso.append(mlb_tentativa)
                return True
            except Exception:
                if tentativa < max_tentativas:
                    logger.warning(
                        f'Falha ao importar {mlb_tentativa} na tentativa {tentativa}. '
                        f'Nova tentativa em {esperar_segundos}s.'
                    )
                    mlb_tentativa = self.solicitar_mlb_correcao(mlb_tentativa)
                    time.sleep(esperar_segundos)
                else:
                    logger.exception(
                        f'Falha definitiva ao importar {mlb_tentativa} apos {max_tentativas} tentativas'
                    )
                    self.mlbs_falha.append(mlb_tentativa)
                    raise RuntimeError(
                        f'Erro na importação da MLB {mlb_tentativa}. Encerrando automação.'
                    )

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
            while True:
                MLB = input('Digite sua MLB(s): ').strip()
                
                if not MLB:
                    print('informe pelo menos uma MLB')
                    logger.warning('Entrada de MLB(s) vazia')
                    continue
                
                possiveis = [item.strip().upper() for item in re.split(r'[,\s;]+', MLB) if item.strip()]
                validos = [item for item in possiveis if re.fullmatch(r'MLB\d+', item)]
                
                if not validos:
                    print('Nenhuma MLB valida encontrada')
                    logger.warning(f'Nenhuma MLB valida na entrada: {MLB}')
                    continue
                
                logger.info(f'MLB(s) coletadas: {validos}')
                return validos
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
    automacao = None
    try:
        logger.info('Iniciando automação')  
        with sync_playwright() as pw: 
            navegador = pw.chromium.launch(headless=False, slow_mo=800)
            contexto = navegador.new_context()

            pagina = contexto.new_page()
            automacao = TinyAutomation(pagina)
            
            automacao.tempo_inicio = time.time()

            automacao.login()

            escolha = automacao.opcao_do_usuario()
            automacao.escolha_ml = escolha
            
            automacao.ir_ao_ml(escolha)
        
            MLBs = automacao.sua_MLBs()
            automacao.mlbs = MLBs
            
            for mlb in MLBs:
                automacao.importar_novamente(mlb, max_tentativas=2, esperar_segundos=2)
        
            automacao.relacionar_ml(escolha)
        
            automacao.logout()

            navegador.close()
            logger.info('Automação finalizada com sucesso')
    except Exception:
        logger.exception('Erro em na automação')
    finally:
        if automacao:
            automacao.print_sumarry()
if __name__ == '__main__':
    main()


