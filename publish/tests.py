from django.test import TestCase
# from django.urls import reverse

# from myapp.models import MyModel
# from myapp.views import MyModelListView, MyModelDetailView

# class MyModelListViewTest(TestCase):
#     def setUp(self):
#         # Create some test data
#         MyModel.objects.create(name='Model 1')
#         MyModel.objects.create(name='Model 2')

#     def test_get(self):
#         # Test the GET request
#         url = reverse('mymodel-list')  # Assuming 'mymodel-list' is the URL name for MyModelListView
#         response = self.client.get(url)
        
#         # Assert that the response has a status code of 200
#         self.assertEqual(response.status_code, 200)
        
#         # Assert that the response contains the correct number of objects
#         self.assertEqual(len(response.context['object_list']), 2)

# class MyModelDetailViewTest(TestCase):
#     def setUp(self):
#         # Create a test object
#         self.model = MyModel.objects.create(name='Model 1')

#     def test_get(self):
#         # Test the GET request
#         url = reverse('mymodel-detail', kwargs={'pk': self.model.pk})  # Assuming 'mymodel-detail' is the URL name for MyModelDetailView
#         response = self.client.get(url)
        
#         # Assert that the response has a status code of 200
#         self.assertEqual(response.status_code, 200)
        
#         # Assert that the response contains the correct object
#         self.assertEqual(response.context['object'], self.model)
