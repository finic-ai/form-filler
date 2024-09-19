from models import InputSchema
from playwright.sync_api import sync_playwright, Playwright
import os
from finicapi import Finic
from dotenv import load_dotenv

load_dotenv(override=True)
FINIC_API_KEY = os.getenv("FINIC_API_KEY")
finic = Finic(
    api_key=FINIC_API_KEY,
)


@finic.workflow_entrypoint(input_model=InputSchema)
def main(input: InputSchema):
    url = input.url
    form_data = input.form_data

    print("Running the Playwright script")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()

        # Navigate to the website and login
        page.goto(url)
        page.wait_for_load_state("networkidle", timeout=10000)

        page.fill('input[name="username"]', form_data.username)
        page.fill('input[name="password"]', form_data.password)
        page.fill('textarea[name="comments"]', form_data.comment)
        # click on the input 
        page.set_input_files('input[type="file"]', files=form_data.file_path)
        page.check('input[type="radio"][value="{}"]'.format(form_data.radio_value))
        for checkbox_value in form_data.checkbox_values:
            page.check('input[type="checkbox"][value="{}"]'.format(checkbox_value))
        page.select_option('select[name="multipleselect[]"]', value=form_data.multi_select_values)
        page.select_option('select[name="dropdown"]', value=form_data.dropdown_value)

        page.click('input[type="submit"]')

        browser.close()
