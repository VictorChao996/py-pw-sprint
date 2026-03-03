
from playwright.sync_api import Page, expect
import pytest

rootPage = 'https://the-internet.herokuapp.com/'

# Basic Page goto
def test_page_title(page:Page):
    page.goto(rootPage)
    assert "Internet" in page.title()


# Go to Login Page
def test_go_to_login_page(page):
    page.goto(rootPage)
    page.get_by_role("Link", name='Form Authentication').click()

    expect(page).to_have_url(rootPage + 'login')
    

@pytest.fixture
def login_page(page: Page)->Page:
    """Login Page Fixture """
    page.goto(rootPage + 'login')
    expect(page).to_have_url(rootPage + 'login')
    
    return page

class TestLoginPage:

    @pytest.mark.parametrize("username, password", [('tomsmith', 'SuperSecretPassword!')])
    def test_login_success(self, username, password, login_page):
        """測試登入成功跳轉"""
        login_page.get_by_label('Username').fill(username)
        login_page.get_by_label('Password').fill(password)
        login_page.get_by_role('button', name='Login').click()

        expect(login_page).to_have_url(rootPage + 'secure')

    @pytest.mark.parametrize("username, password, error_msg_text", [('tomsmith', '123', 'Your password is invalid!'), ('123', '123', 'Your username is invalid!')])
    def test_login_failed(self, username, password, error_msg_text, login_page):
        """測試登入失敗顯示 error message"""
        login_page.get_by_label('Username').fill(username)
        login_page.get_by_label('Password').fill(password)
        login_page.get_by_role('button', name='Login').click()

        err_msg = login_page.locator('#flash')
        expect(err_msg).to_contain_text(error_msg_text)
        login_page.screenshot(path='screenshots/loginpage_error_msg.png')

    def test_screenshot(self, login_page):
        login_page.screenshot(path='screenshots/loginpage.png') # 建立 screenshot
        expect(login_page).to_have_url(rootPage + 'login')
        # ! Python 中的 PageAssertions 沒有 to_have_screenshot() 功能
        # expect(login_page).to_have_screenshot('loginpage.png')

class TestCheckboxPage:
    @pytest.fixture
    def checkbox_page(self, page: Page)->Page:
        page.goto(rootPage + 'checkboxes')
        expect(page).to_have_url(rootPage + 'checkboxes')

        return page

    def test_checkbox(self, checkbox_page: Page):
        checkboxes = checkbox_page.get_by_role("checkbox")
        c1 = checkboxes.nth(0)
        c2 = checkboxes.nth(1)

        c1.check()
        c2.uncheck()

        expect(c1).to_be_checked()
        expect(c2).not_to_be_checked()
        

class TestDropsownPage:
    @pytest.fixture
    def dropdown_page(self, page:Page)->Page:
        page.goto(rootPage + 'dropdown')
        return page
    
    def test_dropdown_page(self, dropdown_page:Page):
        dropdown = dropdown_page.locator('#dropdown')
        dropdown.select_option('1')

        expect(dropdown).to_have_value("1")
        



    

