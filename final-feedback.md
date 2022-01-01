## Feedback on Final Exam

## Temperature Conversion using Robot Framework

**Good Student Code**: [temperature.robot](final/temperature.robot)

This problem was worth 12 points.

Maximum of 6 points (half credit) for writing a separate rule for each conversion, with hardcoded values, such as:

```rf
*** Keywords ***
Temperature 77 Fahrenheit Should be 25 Celsius
    Select From List By Label  id:calFrom      Fahrenheit
    Select From List By Label  id:calTo        Celsius
    Input Text                 name:fromValue  77
    ...etc

Temperature 40 Celsius Should Be 104 Fahrenheit
    Select From List By Label  id:calFrom      Celsius
    Select From List By Label  id:calTo        Fahrenheit
    Input Text                 name:fromValue  25
    ...etc

Temperature 0 Celsius Should Be 273.15 Kelvin
    similar code to the above
```

Points also deducted for:

* -1 using DOM-dependent Xpath expression to locate elements (not necessary, brittle)
* -1 using list index (1, 2, 3) instead of labels (Celsius, Fahrenheit)
* -1 not reading the conversion result from web page
* -1 no test in code that expected == actual result
* -1 not logging actual result to console
   

## Github API Testing using Gherkin

| Points | Criterion  |
|--------|:-----------|
| 3      | User auth scenario correct |
| 6      | User info scenario correct |
| 3      | User repos scenario correct |
| 1      | All steps are implemented  |
| 1      | Env var "Given" step does not hard-code envvar names |
| 1      | `the response contains {var} is "{value}"` is one step, not 4 steps |
| 15     | Total Score |

**Good Student Code**: [github_api_steps.py](final/github_api_steps.py)

You also need a features/environment.py containing:
```python
def before_scenario(context, scenario):
    """Reset some values before each scenario."""
    context.headers = {}
```
if you don't have this file, then in the step code you should test if `context.headers` exists before accessing it, which means an extra if-else in 2 functions.



## Common Problems

1. Building your own "token" auth header instead of using requests library.
   - Bad:
     ```python
     token = os.getenv('GITHUB_TOKEN')
     auth_header = {"Authorization": f"token {token}"}
     response = requests.get(url, headers=auth_header)
     ``` 
     Fails if the environment variable is not set!
   - Better:
     ```python
     # in the @given('I am an authenticated user') step
     from requests.auth import HTTPBasicAuth
     username = os.getenv('GITHUB_USER', '')
     password = os.getenv('GITHUB_TOKEN', '')
     context.auth = HTTPBasicAuth(username, password)

     # in the @when("I get the information for ...") step:
     if context.auth:
         response = requests.get(url, auth=context.auth)
     else:
         response = requests.get(url)
     ```
   
2. Parsing response data in `@when("I query the user info...")`.
  - Good: save the whole response so that other steps can get whatever information they need. Reduces coupling between steps.  Remember the guideline: "*Pass whole object*"? 
    ```python
    context.response = requests.get(url)
    ```
   - Bad (saves only specific attributes):
    ```python
    response = requests.get(url)
    data = response.json()
    context.email = data['email']
    context.name = data['name']
    context.company = data['company']
    context.hireable = data['hireable']
    ```
  - Really Bad: This code is coupled to a completely unrelated step (authentication) and invalidates the authentication test:
    ```python
    data = response.json()
    if context.token is not None:
        context.email = data["email"]
        context.company = data["company"]
        context.name = data["name"]
        context.hireable = data["hireable"]
    else:
        context.email = None
        context.company = None
        context.name = None
        context.hireable = None
    ```

3. Writing separate steps for each user-attribute:
   - Bad:
   ```python
   @then('the response contains name is "{name}"'):
   def step_impl(context, name):
       ...
   @then('the response contains email is "{email}"'):
   def step_impl(context, email):
       ...
   @then('the response contains company is "{company}"'):
   def step_impl(context, company):
       ...
   @then('the response contains hireable is "{hireable}"):
   def step_impl(context, hireable):
   ```
   - Good:
   ```python
   @then('the response contains {attribute} is "{value}"):
   def response_contains(context, attribute, value):
       assert context.response is not None
       data = context.response.json()
       # or   json.loads(context.response.text)
       if value in ['null', 'none', 'None']:
           assert data['attribute'] is None
       else:
           assert str(data[attribute]) == value
   ```
   See below for why use `str(data[attribute]) == value`.

4. Testing non-string values.   
   Some values in the JSON response object for `/users/{username}` contain integer, boolean, and other non-string values.  When you decode the response, the Python dict will have non-string values.  So a step like this may fail:    
```python
   @then('the response contains {attribute} is "{value}"):
   def response_contains(context, attribute, value):
       data = context.response.json() 
       assert data[attribute] == value  <-- FAIL if data[attribute] is not string
   ```
   By default, Behave sets the `value` parameter to a string.  So, compare actual and expected values as strings.
   ```python
       if value in ['null','none','None']:
           # special case: allow diferent words for "null"
           assert data[attribute] is None
       else:
           assert str(data[attribute]) == value
   ```


5. Wrong *semantics* for `Given the environment contains XXX`.
   - Wrong: many people used this step to set a "token" that they use in an Authentication header.  That is incorrect. The `Given I am an authenticated user` step should build an auth header.
   - Correct:
   ```python
   @given('the environment contains {variable}')
   def environment_contains(context, variable):
       # many ways to test this. You should supply default value to getenv.
       assert os.getenv(variable, None), f"{variable} is not defined"
   ```

6. Uninitialized context variables.  Many students set a `context.token` variable in the `Given I am an authenticated user` step.    
   But their code **depends on** this attribute being set:
   ```python
   @when('I query the user information for {username}')
   def query_user_info(context, username):
       # FAILS if context.token is not defined:
       headers = {"Authentication": "token " + context.token}
       ...
   ```
   - Good: create an `environment.py` file in the `features` directory. This is like "setUp" in unittest.
   ```python
   def before_scenario(context, scenario):
       """Reset values to defaults."""
       context.token = ""
   ```
