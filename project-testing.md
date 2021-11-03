## Tests of Project Web Services

### Feedback for WCG

1. Documentation of endpoints is vague: <https://wcg-apis.herokuapp.com/reservation_usage>
   - What is "key"?  An API key?  A Query param? A form param?
   - Using Query Params in a POST is poor security since the URL is often logged.

2. For POST requests it is standard to accept **at least** application/w-www-form-encoded for post data. 
   - Web services typically also accept application/json.

3. What does a POST request return?  Should be:
   ```
   201 Created
   Location: /registration/123456     (if that is the user's id)
   ```

4. How does a client get data for a single registered citizen?


### Feedback for Flamby

Excellent API docs at <https://github.com/flamxby/government/wiki/API-Documentation>.

- Please add auth headers to the examples.

## Design Issue for WCB and Flamby

- How can the service site contact service takers (users)?
- I think ability to contact service takers is **essential**?
- Validate citizen id? See <https://en.wikipedia.org/wiki/Thai_identity_card#Identification_number>. 
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

Python Requests Documentation:
```python
base_url = 'https://wcg-apis/herokuapp.com'

url = base_url + '/registration'
request_params = {'key1': 'value1', 'key2': ['value2', 'value3']}

# send the request_params as query parameters
response = requests.post(url, params=request_params)

# send the request_params as content body
response = requests.post(url, data=request_params)
```

Sending Headers:
```python
headers = {'content-type': 'application/json'}

response = requests.post(url, headers=headers, data=request_params)
```
(setting content-type is not enough)

Sending request body as JSON:
```python
import json
headers = {'content-type': 'application/json'}

# requests library does NOT automatically
# set 'content-type: application/json'
response = requests.post(url, data=json.dumps(request_params))

# same thing, but explicitly add 'content-type: application/json'
```
response = requests.post(url, data=json.dumps(request_params), headers=headers)


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
        self.query_params[citizen_id] = ""
        self.response = requests.post(url, data=self.query_params)
        self.assertEqual(self.response.status_code, 400)
        # delete citizen_id entirely
        del(self.query_params[citizen_id])
        self.response = requests.post(url, data=self.query_params)
        self.assertEqual(self.response.status_code, 400)
```

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
