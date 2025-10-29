import allure
import pytest
from playwright.sync_api import expect, Page

from pages.role_based_login_flow_page import AdminDashboardPage, LoginPage, UserDashboardPage
from utils.allure import attach_screenshot



@allure.id("LF_001")
@allure.severity("high")
@allure.tag("negative")
def test_empty_fields_validation(page: Page):
    login_page = LoginPage(page)
    login_page.navigate_to_login()
    login_page.login("", "")

    attach_screenshot(page)

    expect(login_page.empty_fields_error).to_be_visible()

@allure.id("LF_002")
@allure.severity("high")
@allure.tag("negative")
def test_invalid_credentials_validation(page: Page):
    login_page = LoginPage(page)
    login_page.navigate_to_login()
    login_page.login("wrongUser", "wrongPass")

    attach_screenshot(page)

    expect(login_page.invalid_credentials_error).to_be_visible()


@allure.id("LF_003")
@allure.severity("high")
@allure.tag("positive")
def test_user_login(page: Page):
    login_page = LoginPage(page)
    login_page.navigate_to_login()
    login_page.login("user", "user123")

    user_dashboard_page = UserDashboardPage(page)

    attach_screenshot(page)

    expect(user_dashboard_page.successful_login_message).to_be_visible()
    expect(user_dashboard_page.dashboard).to_be_visible()


@allure.id("LF_004")
@allure.severity("high")
@allure.tag("positive")
def test_admin_login(page: Page):
    login_page = LoginPage(page)
    login_page.navigate_to_login()
    login_page.login("admin", "admin123")

    admin_dashboard_page = AdminDashboardPage(page)

    attach_screenshot(page)

    expect(admin_dashboard_page.successful_login_message).to_be_visible()
    expect(admin_dashboard_page.dashboard).to_be_visible()


@allure.id("LF_005")
@allure.severity("medium")
@allure.tag("positive")
@pytest.mark.parametrize("username, password, dashboard_class", [
    ("user", "user123", UserDashboardPage),
    ("admin", "admin123", AdminDashboardPage)
])
def test_logout(page: Page, username, password, dashboard_class):
    login_page = LoginPage(page)
    login_page.navigate_to_login()
    login_page.login(username, password)
    dashboard = dashboard_class(page)

    attach_screenshot(page, "after login")
    expect(dashboard.logout_button).to_be_enabled()

    dashboard.logout()

    attach_screenshot(page, "after logout")

    expect(login_page.username_input).to_be_visible()
    expect(login_page.password_input).to_be_visible()
    expect(login_page.username_input).to_be_empty()
    expect(login_page.password_input).to_be_empty()
