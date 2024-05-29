import pytest
from main_test.Report_mail import fetch, Send_Mail
from main_test.Dashboard import *
from playwright.sync_api import sync_playwright




def pytest_unconfigure(config):
    dashboard_list = fetch()
    dashboard_main(dashboard_list)
    Send_Mail()
    
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # This hook is called after each test call
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs['page']
        screenshot_path = f"screenshots/{item.nodeid.replace('::', '_')}.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright

@pytest.fixture
def browser(playwright_instance):
    # browser_type = request.param
    browser = playwright_instance.chromium.launch( timeout=60000)
    yield browser
    browser.close()

@pytest.fixture
def context(browser):
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture
def page(context):
    page = context.new_page()
    yield page
    page.close()