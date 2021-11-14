import os
import requests
from behave import given, when, then

@given('the server is started')
def step_impl(context):
    context.base_url = os.getenv(
        'BASE_URL', 
        'http://localhost:8080'
    )
    context.resp = requests.get(context.base_url + '/')
    assert context.resp.status_code == 200


@when(u'I visit the "home page"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I visit the "home page"')


@then(u'I should see "Pet Demo REST API Service"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should see "Pet Demo REST API Service"')


@then(u'I should not see "404 Not Found"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should not see "404 Not Found"')