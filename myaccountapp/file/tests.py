from rest_framework.test import APITestCase


class SnippetTestCase(APITestCase):
    def test_bill_post(self):
        bill_response = self.client.post('/v1/bill/b5e28f84-b397-490a-a741-a1f5fcf91284/file', {
                                                       "url": "/Users/nmanjunatha/Downloads/Image from iOS (4).jpg",
                                                       },
                                         format='json')
        self.assertEqual(bill_response.status_code, 401)
