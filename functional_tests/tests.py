from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time

MAX_WAIT = 10

class NewVsitorTest(LiveServerTestCase):

    def setUp(self):
        path_to_driver = "C:/Users/Utilisateur/chromedriver_win32/bin/chromedriver.exe"
        self.browser = webdriver.Chrome(path_to_driver)

    def tearDown(self):
        self.browser.quit()

    # Auxiliary method 
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)


    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith ouviu falar que agora a aplicação online de lista de tarefas
        # aceita definir prioridades nas tarefas do tipo baixa, média e alta
        # Ela decide verificar a homepage
        self.browser.get(self.live_server_url)
        

        # Ela percebe que o título da página e o cabeçalho mencionam
        # listas de tarefas com prioridade (priority to-do)
        self.assertIn('priority to-do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('priority to-do', header_text)


        # Ela é convidada a inserir um item de tarefa e a prioridade da 
        # mesma imediatamente
        inputbox = self.browser.find_element_by_id('id_new_item_text')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        inputbox = self.browser.find_element_by_id('id_new_item_priority')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter its priority'
        )



        # Ela digita "Comprar anzol" em uma nova caixa de texto
        # e assinala prioridade alta no campo de seleção de prioridades
        inputbox = self.browser.find_element_by_id('id_new_item_text')
        inputbox.send_keys('Comprar anzol')

        inputbox = self.browser.find_element_by_id('id_new_item_priority')
        inputbox.send_keys("prioridade alta")




        # Quando ela tecla enter, a página é atualizada, e agora
        # a página lista "1 - Comprar anzol - prioridade alta"
        # como um item em uma lista de tarefas
        inputbox = self.browser.find_element_by_id('id_add_new_item')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.wait_for_row_in_list_table('1 - Comprar anzol - prioridade alta')


        # Ainda continua havendo uma caixa de texto convidando-a a 
        # acrescentar outro item. Ela insere "Comprar cola instantâne"
        # e assinala prioridade baixa pois ela ainda tem cola suficiente
        # por algum tempo
        inputbox = self.browser.find_element_by_id('id_new_item_text')
        inputbox.send_keys('Comprar cola instantâne')

        inputbox = self.browser.find_element_by_id('id_new_item_priority')
        inputbox.send_keys("prioridade baixa")

        inputbox = self.browser.find_element_by_id('id_add_new_item')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)


        # A página é atualizada novamente e agora mostra os dois
        # itens em sua lista e as respectivas prioridades
        self.wait_for_row_in_list_table('1 - Comprar anzol - prioridade alta')
        self.wait_for_row_in_list_table('2 - Comprar cola instantâne - prioridade baixa')


        # Edith se pergunta se o site lembrará de sua lista. Então
        # ela nota que o site gerou um URL único para ela -- há um 
        # pequeno texto explicativo para isso.

        # self.fail('Finish the test!')

        # Ela acessa essa URL -- sua lista de tarefas continua lá.


# O maior desafio de nossa história de usuário é lidar com as URLs distintas para cada novo usuário do nosso sistema. 
# A necessidade é que tenhamos URLs únicas para cada usuário consultar a sua própria lista de tarefas.

# folha de rascunho de itens que precisam ser resolvidos a fim de implementarmos a história de
# usuário por completa:
# - Ajustar o modelo para que itens sejam associados a listas distintas
# - Adicionar URLs exclusivos para cada lista, por exemplo, como /lists/<identificador da lista>/
# - Adicionar um URL para criar uma lista via POST, por exemplo, como /lists/new
# - Adicionar URL para acrescentar um novo item em uma lista existente, por exemplo,  como /lists/<identificador da lista>/add_item

# Antes de iniciarmos com as implementações, o primeiro passo é modificarmos nosso teste funcional, garantindo que tenhamos um 
# mecanismo para detectar possíveis quebras no código.
# Desse modo, o nosso teste funcional ficará conforme abaixo. Basicamente, alteramos o nome do método de teste anterior de 
# test_can_start_a_list_and_retrieve_it_later para test_can_start_a_list_for_one_user e incluímos um novo método de teste 
# para avaliar a característica de múltiplos usuários


    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith inicia uma nova lista de tarefas
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item_text')
        inputbox.send_keys('Comprar anzol')
        inputbox = self.browser.find_element_by_id('id_new_item_priority')
        inputbox.send_keys("prioridade alta")
        inputbox = self.browser.find_element_by_id('id_add_new_item')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1 - Comprar anzol - prioridade alta')

        #Ela percebe que sua lista te um URL único
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        #Agora um novo usuário, Francis, chega ao site

        ## Usamos uma nova versão do nagegador para garantir que nenhuma 
        ## informação de Edith está vindo de cookies, etc
        
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis acessa a página inicial. Não há sinal da lista de Edith
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis inicia uma nova lista inserindo um novo item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis obtém seu próprio URL exclusivo
        francis_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.assertNotEqual( francis_list_url, edith_list_url)

        # Novamente não há sinal algum da lista de Edith
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Fim
