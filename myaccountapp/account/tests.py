from rest_framework.test import APITestCase
import pdb

class SnippetTestCase(APITestCase):
    def test_post(self):
        response = self.client.post('/v1/user/', { 'email': 'nishanth@gmail.com',
                                                   'first_name': 'nishanth',
                                                   'last_name': 'm',
                                                   'password': 'Abcd123456@' },
                                    format='json')
        pdb.set_trace()
        self.assertEqual(response.status_code, 201)