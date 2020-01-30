from rest_framework.test import APITestCase


class SnippetTestCase(APITestCase):
    def test_bill_post(self):
        bill_response = self.client.post('/v1/bill/', {"vendor": "Northeastern University",
                                                       "bill_date": "2020-01-06",
                                                       "due_date": "2020-01-12",
                                                       "amount_due": 7000.51,
                                                       "categories": [
                                                           "college",
                                                           "tuition",
                                                           "spring2020"
                                                       ],
                                                       "paymentStatus": "paid"
                                                       },
                                         format='json')
        self.assertEqual(bill_response.status_code, 401)
