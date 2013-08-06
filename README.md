zooz-python
===========

Python interface to the [ZooZ](http://www.zooz.com) Extended Server API.

Already implemented:

* Open a new transaction.

* Get info of transaction by id.
* Get all transactions done by an email.


Enable sandbox mode
--------------------

By default requests will be done to the production ZooZ server, to enable sandbox mode, just modify `ZOOZ_SANDBOX` to `True`

```python
import zooz.client as z
z.ZOOZ_SANDBOX = True
```


Getting authentication info
----------------------------

To get requests authorized, this info is needed, available at your app's info:

* App unique ID
* App key

For extended API:

* Developer ID: the email used to log in [developers portal](https://app.zooz.com/portal/)
* API Key: available at [My Account](https://app.zooz.com/portal/PortalController?cmd=myAccount)


Doing requests!
---------------

Client has been splitted in two separated client, one for mobile-web, `client.ZoozRequest` and
other for the Extended Server API, `client.ZoozRequestExtended`

To open a transaction and get the token:

```python
import zooz.client as z

request = z.ZoozRequest(unique_id='YOUR_UNIQUE_ID', app_key='YOUR_APP_KEY')

# extra dict, is used to attach more info to the transaction, see ZooZ Mobile documentation
request.open_transaction(amount, currency_code, extra)
# if succedded , returns a dict with 'token' key
```

To use Extended Server API:

```python
import zooz.client as z

request = z.ZoozRequestExtended(developer_id='YOUR_EMAIL', api_key='YOUR_API_KEY')

# to get a transaction info using its ID:
request.get_transaction('TRANSACTION_ID')

# to get a list of transactions done by an user
request.get_transactions(user_email='USER_EMAIL')
```

Testing
--------

Before calling tests, you will need to add some keys to your environment with
ZooZ credentials:

* `ZOOZ_UNIQUE_ID` with your unique ID.
* `ZOOZ_APP_KEY` with your APP key

```bash
$ python setup.py test
```
