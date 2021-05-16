from django.urls import resolve
from django.test import TestCase
from lists.views import home_page

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEquals(found.func, home_page)

    # nossa aplicação terá que exibir algo para o usuário, efetivamente.
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEquals(Item.objects.count(), 0)


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item', 'item_priority': "prioridade baixa"})
        self.assertEquals(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEquals(new_item.text, 'A new list item')
        self.assertEquals(new_item.priority, "prioridade baixa")

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item', 'item_priority': "prioridade baixa"})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')


class ListViewTest(TestCase):
    def test_displays_all_list_itens(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', priority="prioridade baixa", list=list_)
        Item.objects.create(text='itemey 2', priority="prioridade média", list=list_)
        Item.objects.create(text='itemey 3', priority="prioridade alta", list=list_)

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertContains(response, 'itemey 3')
        self.assertContains(response, 'prioridade baixa')
        self.assertContains(response, 'prioridade média')
        self.assertContains(response, 'prioridade alta')


    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')


from lists.models import Item, List

class ListAndItemModelTest(TestCase): #

    def test_saving_and_retriving_items(self):
        list_ = List() #
        list_.save() #

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.priority = 'prioridade baixa'
        first_item.list = list_ #
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.priority = 'prioridade alta'
        second_item.list = list_ #
        second_item.save()

        saved_list = List.objects.first() #
        self.assertEquals(saved_list, list_) #

        saved_items = Item.objects.all()
        self.assertEquals(saved_items.count(),2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEquals(first_saved_item.text, 'The first (ever) list item')
        self.assertEquals(second_saved_item.text, 'Item the second')
        self.assertEquals(first_saved_item.priority, 'prioridade baixa')
        self.assertEquals(second_saved_item.priority, 'prioridade alta')
        self.assertEquals(first_saved_item.list, list_)    #
        self.assertEquals(second_saved_item.list, list_) #
