from playwright.sync_api import Page, expect
import pytest

class LoginPage:
    URL = "https://the-internet.herokuapp.com/login"
    FLASH_SUCCESS_TEXT = "You logged into a secure area!"
    FLASH_USERNAME_FAIL_TEXT = "Your username is invalid!"
    FLASH_PASSWORD_FAIL_TEXT = "Your password is invalid!"

    def __init__(self, page:Page):
        self.page = page

        # Page Element
        self.username_input = page.get_by_label('Username')
        self.password_input = page.get_by_label('Password')
        self.login_btn = page.get_by_role('button', name='Login')
        self.message = page.locator('#flash')

    def navigate(self):
        self.page.goto(self.URL)
        return self

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_btn.click()
        return self
    
    # 實務上可能不會這樣寫, 讓 POM 只負責操作, Test 只負責驗證, 各司其職
    def expect_success(self):
        expect(self.message).to_contain_text(self.FLASH_SUCCESS_TEXT)

    def expect_username_fail(self):
        expect(self.message).to_contain_text(self.FLASH_USERNAME_FAIL_TEXT)
    
    def expect_password_fail(self):
        expect(self.message).to_contain_text(self.FLASH_PASSWORD_FAIL_TEXT)

    


@pytest.fixture
def login_page(page)->LoginPage:
    """建立 LoginPage object fixture"""
    return LoginPage(page).navigate()

def test_login_success(login_page):
    (username, password) = ("tomsmith", "SuperSecretPassword!")
    login_page.login(username, password)
    login_page.expect_success()


def test_username_login_fail(login_page):
    login_page.login("123", "123")
    login_page.expect_username_fail()

def test_password_login_fail(login_page):
    login_page.login("tomsmith", "123")
    login_page.expect_password_fail()


#------

class DynamicLoadingPage:
    URL = 'https://the-internet.herokuapp.com/dynamic_loading/1'

    def __init__(self, page:Page):
        self.page = page
        self.start_btn = page.get_by_role('button', name='Start')
        self.finish_txt = page.locator('#finish')
    def navigate(self):
        self.page.goto(self.URL)
        return self
    
    def test_navigate(self):
        with self.page.expect_response("**/dynamic_loading/*") as response_info:
            self.navigate()
        assert response_info.value.ok
        assert response_info.value.status == 200

    def press_start_btn(self):
        self.start_btn.click()

    def wait_for_text(self):
        self.finish_txt.wait_for(state='visible')

    def get_result_text(self):
        self.wait_for_text()
        return self.finish_txt.inner_text()

    def expect_result_text(self, text: str):
        expect(self.finish_txt).to_have_text(text)

@pytest.fixture
def dynamic_page(page)->DynamicLoadingPage:
    return DynamicLoadingPage(page).navigate()

def test_dynamic_page_finish_text(dynamic_page):
    dynamic_page.press_start_btn()
    assert dynamic_page.get_result_text() == 'Hello World!'

def test_dynamic_page_1_naviagting(dynamic_page):
   dynamic_page.test_navigate()
