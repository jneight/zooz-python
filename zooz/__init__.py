# coding=utf-8

"""
   Copyright 2013 Javier Cordero Martinez

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

__version__ = '0.3'

import requests
import logging
import time
logger = logging.getLogger(__name__)

try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse

try:
    import ujson as json
except ImportError:
    import json

ZOOZ_SANDBOX = False
ZOOZ_API_VERSION = '1.0.4'
ZOOZ_URLS = {
    'production': 'https://app.zooz.com/',
    'sandbox': 'https://sandbox.zooz.co/',
}


def backoff_retry(retries=0, delay=1, backoff=2):
    """
        Based on: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

        In case of a connection error, will try to retry the function.

            retries: number of tries, can be 0
            delay:  sets the initial delay in seconds for the first try.
            backoff: factor used to increase the delay after new errors
    """
    if backoff <= 1:
        raise ValueError("backoff must be 0 or greater")
    if retries < 0:
        raise ValueError("retries must be greater than 0")
    if delay <= 0:
        raise ValueError("delay must be greater than 0")

    def wrapper(f):
        def retry_f(*args, **kwargs):
            try:
                return f(*args, **kwargs)  # first attempt
            except requests.ConnectionError:
                for t in range(retries):
                    try:
                        wait = delay * backoff * (t + 1)
                        time.sleep(wait)
                        return f(*args, **kwargs)  # new attempt
                    except requests.ConnectionError:
                        pass
                raise
        return retry_f
    return wrapper


class ZoozException(Exception):
    """
        Extends Exception class adding:

            message: error message returned by ZooZ
            status_code: response status returned by ZooZ
    """
    def __init__(self, message, status_code):
        Exception.__init__(self, message)
        self.status_code = status_code


class ZoozRequest(object):
    """
        Client for the ZooZ Extended Server API

        Go to https://app.zooz.com/portal/PortalController?cmd=resources to
        see complete API documentation

        For authentication, some keys are needed:

            unique_id: as registered in the ZooZ developer portal
            app_key: as received upon registration

        In case you want to use Extended server API:

            developer_id: developer email used to log in ZooZ Developers portal
            app_key: Server API Key found in ZooZ portal -> My Account

        By default, requests will be done to the 'production' ZooZ servers,
        so all transactions and payment will be real, to allow 'sandbox' mode
        just change the global variable ZOOZ_SANDBOX

            ZOOZ_SANDBOX = True
    """
    def __init__(
            self, developer_id=None, api_key=None, unique_id=None,
            app_key=None):
        self.developer_id = developer_id
        self.api_key = api_key
        self.unique_id = unique_id
        self.app_key = app_key
        self.requests = requests.Session()

    def _get_url(self):
        global ZOOZ_SANDBOX
        global ZOOZ_URLS

        if ZOOZ_SANDBOX:
            return ZOOZ_URLS['sandbox']
        else:
            return ZOOZ_URLS['production']

    @property
    def get_url_extended(self):
        """
            Returns the final URI needed to do requests to extended API
        """
        return self._get_url() + 'mobile/ExtendedServerAPI'

    @property
    def get_url(self):
        """
            Returns the final URI needed to do requests to the secured servlet
        """
        return self._get_url() + 'mobile/SecuredWebServlet'

    def add_authentication_extended(self):
        headers = {
            'ZooZDeveloperId': self.developer_id,
            'ZooZServerAPIKey': self.api_key,
        }
        return headers

    def add_authentication(self):
        headers = {
            'ZooZUniqueID': self.unique_id,
            'ZooZAppKey': self.app_key,
            'ZooZResponseType': 'NVP'
        }
        return headers

    @backoff_retry(retries=5)
    def post(self, payload, headers):
        """
            Add authentication headers to the request
        """
        return self.requests.post(self.get_url, data=payload, headers=headers)

    def get_transaction(self, transaction_id):
        """
            Get the info about a transaction using its ID

            :returns: a dict with two keys:
                'ResponseStatus': 0 if all is correct
                'ResponseObject': transaction info, see ZooZExtendedAPI doc.

            :raises: ZoozException in case request fails
        """
        assert transaction_id

        payload = {
            'cmd': 'getTransactionDetails',
            'ver': ZOOZ_API_VERSION,
            'transactionID': transaction_id,
        }
        headers = self.add_authentication_extended()
        logger.debug('[ZOOZ] get transaction with payload: %s', payload)
        response = self.post(payload, headers).json()
        if int(response['ResponseStatus']) != 0:
            raise ZoozException(
                response['ResponseObject']['errorMessage'],
                response['ResponseStatus'])
        return response

    def get_transactions(self, user_email, from_date=None, to_date=None):
        """
            Get the list of transaction generated by an user.

            Allows filtering by date, date should be in the format: YYYY-mm-dd

            :returns: a dict with two keys:
                'ResponseStatus': 0 if all is correct.
                'ResponseObject': transaction info, see ZooZExtendedAPI doc.

            :raises: ZoozException in case request fails
        """
        assert user_email

        payload = {
            'cmd': 'getTransactionDetailsByPayerEmail',
            'ver': ZOOZ_API_VERSION,
            'email': user_email,
            'fromDate': from_date,
            'toDate': to_date,
        }
        headers = self.add_authentication_extended()
        logger.debug('[ZOOZ] get transactions for user: %s', payload)
        response = self.post(payload, headers).json()
        if int(response['ResponseStatus']) != 0:
            raise ZoozException(
                response['ResponseObject']['errorMessage'],
                response['ResponseStatus'])
        return response

    def open_transaction(self, amount, currency_code, extra=None):
        """
            Open a transaction using a secured channel to ZooZ.

                amount: The amount to pay.
                currency_code: ISO code of the currency used to pay.

                Optional parametres can be used, use extra and a dict
                for a list of parameters name, see
                    ZooZ mobile web developer guide.

            :returns: Unique token used to identify the transaction.

                'statusCode': If equals to zero, request succeeded
                'errorMessage': Will contain the error message
                'token': Token generated

            :raises: ZoozException in case request fails
        """

        payload = {
            'cmd': 'openTrx',
            'amount': amount,
            'currencyCode': currency_code,
        }

        if extra:
            payload.update(extra)

        headers = self.add_authentication()
        logger.debug('[ZOOZ] open transaction: %s', payload)
        response = self._parse_response_nvp(self.post(payload, headers).text)
        if int(response['statusCode']) != 0:
            raise ZoozException(
                response['errorMessage'], response['statusCode'])
        return response

    def _parse_response_nvp(self, response):
        """
            parse_qs will build a dictionary of {key: [list]}, this will return
            a plain dict
        """
        response_dict = urlparse.parse_qs(response, keep_blank_values=True)

        return {k: v[0] for (k, v) in response_dict.items()}
