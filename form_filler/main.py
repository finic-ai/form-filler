from models import InputSchema
from playwright.sync_api import sync_playwright, Playwright
import os
import json
from dotenv import load_dotenv

load_dotenv(override=True)

def main():
    with open("input.json", "r") as f:
        input = json.load(f)
    
    url = input["url"]
    form_data = input["form_data"]

    print("Running the Playwright script")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        
        ### Uncomment this line when you're ready to connect to Finic Browser
        # browser = p.chromium.connect(cdp="wss://browser.finic.io/")
        
        page = browser.new_page()

        # Navigate to the website and login
        page.goto(url)
        page.wait_for_load_state("networkidle", timeout=10000)

        page.fill('input[name="username"]', form_data["username"])
        page.fill('input[name="password"]', form_data["password"])
        page.fill('textarea[name="comments"]', form_data["comment"])
        # click on the input 
        page.set_input_files('input[type="file"]', files=form_data["file_path"])
        page.check('input[type="radio"][value="{}"]'.format(form_data["radio_value"]))
        for checkbox_value in form_data["checkbox_values"]:
            page.check('input[type="checkbox"][value="{}"]'.format(checkbox_value))
        page.select_option('select[name="multipleselect[]"]', value=form_data["multi_select_values"])
        page.select_option('select[name="dropdown"]', value=form_data["dropdown_value"])

        page.click('input[type="submit"]')

        # Check if page confirms our success
        success_message = page.locator('h1:has-text("Processed Form Details")')
        if success_message.is_visible():
            print("Form submission successful")
        else:
            print("Form submission was not successful")

        browser.close()
