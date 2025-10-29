from pages import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_input = page.get_by_role("textbox", name="Username")
        self.password_input = page.get_by_role("textbox", name="Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.empty_fields_error = page.get_by_role("alert").filter(has_text="Both fields are required")
        self.invalid_credentials_error = page.get_by_role("alert").filter(has_text="Invalid username or password")

    def navigate_to_login(self):
        self.open("login-flow")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

