## Tests of Project Web Services

### Feedback for WCG

1. Documentation of endpoints is vague: <https://wcg-apis.herokuapp.com/reservation_usage>
   - What is "key"?  An API key?  A Query param? A form param?
   - Using Query Params in a POST is poor security since the URL is often logged.

2. For POST requests to the `/registration` endpoint, you should encourage users to send data using a **request body** encoded as `application/w-www-form-encoded` (this already works) or `application/json`.

3. What does a POST request return?  Should be:
   ```
   201 Created
   Location: /registration/123456     (if that is the user's id)
   ```

4. (Optional) Response to a POST does not need a body. If you want to send a body then send back the original data as JSON, but omit or mask sensitive data:
   ```
   201 Created
   Location: /registration/123456     (if that is the user's id)
   Content-type: application/json

   { citizen_id: "xxxxxxx123456", name="Fatalai", surname="Jon", ...}
   ```
5. How does a web service client get data for a single registered citizen?


### Reason NOT to send /registration data as query parameters.

Your API suggests sending POST /registration like this:
```
https://site-url/registration?citizen_id=1234567890123&name=xxxx&surname=xxx
```

Two problems with sending data as query parameters:

1. The URL can potentially exceed the server's maximum length (8177 for Apache and Nginx). This will result in a 413 or 414 error.
   - Note that data will be encoded as UTF-8, which can be 5-7 times longer than the original data (think: encoding of Thai characters)! 
   - Web servers typically **log** the request URLs.  These logs are in plain text and not well protected. Someone could potentially steal sensitive info.  It happened to Facebook.


### Feedback for Flamby

Excellent API docs at <https://github.com/flamxby/government/wiki/API-Documentation>.

- Please add auth headers to the examples.

## Design Issue for WCB and Flamby

- How can the service site contact service takers (users)?
- I think ability to contact service takers is **essential**?
- Validate Thai citizen id? See <https://en.wikipedia.org/wiki/Thai_identity_card#Identification_number>. 
  - Last digit is a checksum
  - <https://mynoz.wordpress.com/2006/05/01/how-to-cal-the-last-digit-of-thai-citizen-id-card/>
  - <https://github.com/jukbot/thai-citizen-id-validator/>

```javascript
export default function ThaiNationalID (id) {
  if (!/^[0-9]{13}$/g.test(id)) {
    return false
  }
  let i;
  let sum = 0;
  for ((i = 0), (sum = 0); i < 12; i++) {
    sum += Number.parseInt(id.charAt(i)) * (13 - i)
  }
  const checkSum = (11 - sum % 11) % 10
  if (checkSum === Number.parseInt(id.charAt(12))) {
    return true
  }
  return false
}
```

### Anusid Tests of WCG

Good tests but code is hard to read, many values hard-coded in strings.

```python
def get_api(remove_param, replace):
    URL = "https://wcg-apis.herokuapp.com/registration?citizen_id=1116789838901&name=Benjamin&surname=Lee&birth_date=1999-05-17&occupation=bartender&address=Bangkok"
```

Python Requests Usage:
```python
import requests
import json     # for json encoded requests
base_url = 'https://wcg-apis/herokuapp.com'

url = base_url + '/registration'
testdata = {'citizen_id': '1234567890123', 'name': "Harry", 'surname': ...}

# send the request_params as query parameters (bad)
response = requests.post(url, params=testdata)

# send the request_params as content body (good)
response = requests.post(url, data=testdata)

# send the request_params as content body using JSON (good)
headers = {'content-type': 'application/json'}
response = requests.post(url, 
                         data=json.dumps(testdata),
                         headers=headers)
```

Sending Headers:
```python
headers = {'content-type': 'application/x-www-application-urlencoded'}

response = requests.post(url, headers=headers, data=testdata)
```

Example code:
```python

    def setUp(self):
        self.base_url = 'https://wcg-apis.herokuapp.com'
        self.data = {'citizen_id': '1116789838901',
                     'name': 'Benjamin',
                     'surname': 'Lee',
                     'birth_date': '1999-05-17',
                     'occupation': 'bartender',
                     'address': 'Bangkok'
                     }

    def test_registration_missing_citizen_id(self):
        """Test registration with missing citizen_id."""
        url = self.base_url + '/registration'
        # send an empty citizen_id
        self.data[citizen_id] = ""
        self.response = requests.post(url, data=self.data)
        self.assertEqual(self.response.status_code, 400)
        # omit the citizen_id entirely
        del(self.data[citizen_id])
        self.response = requests.post(url, data=self.data)
        self.assertEqual(self.response.status_code, 400)
```

More tests to try:

- send the `name=` parameter twice in same request (this is legal in HTTP)
- send a valid request with body encoded as x-www-form-urlencoded. The response should be 201 (not 200).
- send a valid request with body encoded as JSON. Does it succeed?
- register the same `citizen_id` twice.

## URLs

WCG
* Service: https://wcg-apis.herokuapp.com/
* Brief Doc: https://wcg-apis.herokuapp.com/ 
* OpenAPI: https://wcg-apis.herokuapp.com/api-doc/

Flamby
* Service: https://flamxby.herokuapp.com/
* OpenAPI: https://flamxby.herokuapp.com/docs
* Full Docs: https://github.com/flamxby/government/wiki/API-Documentation




## Reference

- [Make a Request](https://docs.python-requests.org/en/latest/user/quickstart/#make-a-request) in [Python Requests Quickstart](https://docs.python-requests.org/en/latest/user/quickstart/) 
