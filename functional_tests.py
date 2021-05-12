from selenium import webdriver
import unittest

class NewVsitorTest(unittest.TestCase):

    def setUp(self):
        path_to_driver = "C:/Users/Utilisateur/chromedriver_win32/bin/chromedriver.exe"
        self.browser = webdriver.Chrome(path_to_driver)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith ouviu falar de uma nova aplicação online interessante
        # para lista de tarefas. Ela decide verificar a homepage

        self.browser.get("http://localhost:8000")

        # Ela percebe que o título da página e o cabeçalho mencionam
        # listas de tarefas (to-do)

        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # Ela é convidada a inserir um item de tarefa imediatamente

        # Ela digita "Buy peacock feathers" (Comprar penas de pavão)
        # em uma nova caixa de texto (o hobby de Edith é fazer iscas
        # para pesca com fly)

        # Quando ela tecla enter, a página é atualizada, e agora
        # a página lista "1 - Buy peacock feathers" como um item em 
        # uma lista de tarefas

        # Ainda continua havendo uma caixa de texto convidando-a a 
        # acrescentar outro item. Ela insere "Use peacock feathers 
        # make a fly" (Usar penas de pavão para fazer um fly - 
        # Edith é bem metódica)

        # A página é atualizada novamente e agora mostra os dois
        # itens em sua lista

        # Edith se pergunta se o site lembrará de sua lista. Então
        # ela nota que o site gerou um URL único para ela -- há um 
        # pequeno texto explicativo para isso.

        # Ela acessa essa URL -- sua lista de tarefas continua lá.

        # Satisfeita, ela volta a dormir

if __name__ == '__main__':
    unittest.main()