# coding=utf-8

import os
import unittest

import zooz.client as z
z.ZOOZ_SANDBOX = True


class ZoozRequestTest(unittest.TestCase):
    def setUp(self):
        try:
            self.unique_id = os.environ['ZOOZ_UNIQUE_ID']
            self.app_key = os.environ['ZOOZ_APP_KEY']
            self.client = z.ZoozRequest(
                unique_id=self.unique_id, app_key=self.app_key)
        except:
            raise Exception('INVALID KEYS')

    def test_urls(self):
        """
            Check client is using sandbox urls
        """
        self.assertTrue('sandbox.' in self.client.get_url)

    def test_open_transaction(self):
        self.assertIn('token', self.client.open_transaction(
            amount=12, currency_code='GBP'))

        with self.assertRaises(z.ZoozException):
            self.client.open_transaction(
                amount='invalid number', currency_code='GBP')

        with self.assertRaises(z.ZoozException):
            self.client.open_transaction(
                amount=12, currency_code='INVALID')
