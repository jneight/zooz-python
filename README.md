zooz-python
===========

Python interface to the [ZooZ](http://www.zooz.com) Extended Server API.

For now, only getting transaction info is implemented.


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

```python
import zooz

request = zooz.ZoozRequest(developer_id='YOUR_EMAIL', api_key='YOUR_API_KEY')

# to get a transaction info using its ID:
request.get_transaction('TRANSACTION_ID')

# to get a list of transactions done by an user
request.get_transactions(user_email='USER_EMAIL')
```
