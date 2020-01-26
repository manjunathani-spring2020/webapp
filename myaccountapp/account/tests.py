from rest_framework.test import APITestCase


class SnippetTestCase(APITestCase):
    def test_post(self):
        response = self.client.post('/v1/user/', {'email': 'nishanth@gmail.com',
                                                  'first_name': 'nishanth',
                                                  'last_name': 'm',
                                                  'password': 'Abcd123456@'},
                                    format='json')
        self.assertEqual(response.status_code, 201)
