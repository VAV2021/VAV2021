from behave import *
from decouple import config
import requests


def parse_custom_type(text):
    """Convert expected non-string values."""
    if text == "null" or text == "None":
        return None
    elif text.lower() == "true":
        return True
    elif text.lower() == "false":
        return False
    return text

register_type(custom_type=parse_custom_type)

@given('the environment contains {key}')
def set_environment(context, key):
    """The key should be present as an environment variable."""
    assert config(key) != None

@given('I am an authenticated user')
def authenticated_user(context):
    token = config('GITHUB_TOKEN', '')
    context.headers = { "Authorization": f"token {token}" }

@given('I am not an authenticated user')
def unauthenticated_user(context):
    """This is also set in environment.py to avoid undefined variable."""
    context.headers = {}

@when('I query the user information for "{username}"')
def query_user_information(context, username):
    url = f'https://api.github.com/users/{username}'
    context.response = requests.get(url, headers=context.headers)

@when('I query the repositories for "{username}"')
def query_repo_information(context, username):
    url = f'https://api.github.com/users/{username}/repos'
    context.response = requests.get(url, headers=context.headers)

@then('the response contains {key} is "{expected:custom_type}"')
def check_result(context, key, expected):
    actual = context.response.json()[key]
    assert expected == actual

@then('the response contains these repositories')
def user_has_repositories(context):
    # the response is an array of JSON objects (dicts), 
    # each object has data for one repository in the form:
    # {"name": "repo-name", ...},
    data = context.response.json()
    repositories = [repo["name"] for repo in data]
    # Each row in context.table should have 
    # a `repo_name` key with the expected repo name
    for row in context.table:
        assert row['repo_name'] in repositories
