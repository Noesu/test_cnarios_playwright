from pages import BasePage
from pages.role_based_login_flow_page.mixins import LogoutMixin


class AdminDashboardPage(LogoutMixin, BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.successful_login_message = page.get_by_role("alert").filter(has_text="You are logged in as ADMIN")
        self.dashboard = page.get_by_text("Admin Dashboard", exact=True)
