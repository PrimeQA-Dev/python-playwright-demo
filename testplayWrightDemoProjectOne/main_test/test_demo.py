import logging
from playwright.sync_api import expect


def test_one(page):
    page.goto("https://www.saucedemo.com/")
    expect(page.get_by_text('Get Started')).to_be_visible()
    logging.info("Get Started is visible")

def test_two(page):
    page.goto("https://www.saucedemo.com/")     
    username = page.locator('input[name="user-name"]')
    username.fill("standard_user")
    password = page.locator('input[name="password"]')
    password.fill("secret_sauce")
    page.locator('input[name="login-button"]').click()
    add_to_cart_product = page.locator('button[name="add-to-cart-sauce-labs-bike-light"]')
    if add_to_cart_product.is_visible():
        add_to_cart_product.click()
        logging.info("Product is added to cart")
    else:
        logging.info("Add to cart button is not visible")

def test_three(page):
    page.goto("https://www.saucedemo.com/")
    username = page.locator('input[name="user-name"]')
    username.fill("standard_user")
    password = page.locator('input[name="password"]')
    password.fill("secret_sauce")
    page.locator('input[name="login-button"]').click()
    add_to_cart_product = page.locator('button[name="add-to-cart-sauce-labs-bike-light"]')
    if add_to_cart_product.is_visible():
        add_to_cart_product.click()
        logging.info("Product is added to cart")
    else:
        logging.info("Add to cart button is not visible")

    


