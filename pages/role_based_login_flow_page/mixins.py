class LogoutMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logout_button = self.page.get_by_role("button", name="Logout")

    def logout(self):
        self.logout_button.click()