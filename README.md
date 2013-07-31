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
import zooz
zooz.ZOOZ_SANDBOX = True
```


Getting authentication info
----------------------------

To get requests authorized, this info is needed:

* developer ID: the email used to log in [developers portal](https://app.zooz.com/portal/)
* API Key: available at [My Account](https://app.zooz.com/portal/PortalController?cmd=myAccount)


Doing requests!
---------------

To open a transaction and get the token:

```python
import zooz

request = zooz.ZoozRequest(unique_id='YOUR_UNIQUE_ID', app_key='YOUR_APP_KEY')

# extra dict, is used to attach more info to the transaction, see ZooZ Mobile documentation
request.open_transaction(amount, currency_code, extra)
# if succedded , returns a dict with 'token' key
```

To use Extended Server API:

```python
import zooz

request = zooz.ZoozRequest(developer_id='YOUR_EMAIL', api_key='YOUR_API_KEY')

# to get a transaction info using its ID:
request.get_transaction('TRANSACTION_ID')

# to get a list of transactions done by an user
request.get_transactions(user_email='USER_EMAIL')
```


