import pytest
from PageObjects.A_loginpage import LoginPage

class Test_001_Login:
    def test_homepage(self, login):
        page = login  # logged-in Playwright page
        lp = LoginPage(page)
