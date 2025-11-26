import pytest
from playwright.sync_api import sync_playwright, ViewportSize
from PageObjects.Login_Page.A_loginpage import LoginPage
from Utilities.ReadProperties import ReadConfig
from Utilities.BaseHelpers import BaseHelper
from datetime import datetime
from pytest_html import extras

import os
import re


# --------------------------
# CLI Options
# --------------------------
def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chromium",
                     help="Browser: chromium/firefox/webkit")
    parser.addoption("--region", action="store", default="Test",
                     help="Region: AP/ME/US/EU/Test")
    parser.addoption("--headless", action="store_true",
                     help="Run in headless mode")


# --------------------------
# Playwright Instance
# --------------------------
@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as pw:
        yield pw


# --------------------------
# Launch Fresh Browser per Test
# --------------------------
@pytest.fixture(scope="function")
def browser(playwright_instance, request):
    browser_name = request.config.getoption("--browser_name")
    headless = request.config.getoption("--headless")

    if browser_name.lower() == "chromium":
        browser = playwright_instance.chromium.launch(headless=headless)
    elif browser_name.lower() == "firefox":
        browser = playwright_instance.firefox.launch(headless=headless)
    elif browser_name.lower() == "webkit":
        browser = playwright_instance.webkit.launch(headless=headless)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    yield browser
    browser.close()


# --------------------------
# Fresh Page for Every Test
# --------------------------
@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context(
        viewport=ViewportSize(width=1470, height=720)
    )
    page = context.new_page()
    page.set_default_timeout(10000)
    yield page
    context.close()


# --------------------------
# Login Fixture (Optional)
# --------------------------
@pytest.fixture(scope="function")
def login(page, request):
    region = request.config.getoption("--region")

    url = ReadConfig.getURL(region)
    client_id = ReadConfig.getClientID(region)
    username = ReadConfig.getUsername(region)
    password = ReadConfig.getPassword(region)

    print(f"\n➡️ Launching URL: {url} ({region})")
    page.goto(url)

    lp = LoginPage(page)
    lp.setClientid(client_id)
    lp.setUserName(username)
    lp.setPassword(password)
    lp.clickLogin()

    helper = BaseHelper(page)
    helper.verify_page_url("/dashboard", description="Dashboard")

    yield page


# ------------------------------
# Custom HTML Report Title
# ------------------------------
@pytest.mark.optionalhook
def pytest_html_report_title(report):
    report.title = "🚀 Cflow Playwright Automation Report"


# ------------------------------
# Clean Metadata (Remove Environment Info)
# ------------------------------
@pytest.mark.optionalhook
def pytest_configure(config):
    config._metadata = {}
    config.option.metadata = {}
    config._environment = False


@pytest.mark.optionalhook
def pytest_metadata(metadata):
    metadata.clear()


# ------------------------------
# Add Custom Header to HTML Report
# ------------------------------
# @pytest.mark.optionalhook
# def pytest_html_results_summary(prefix, summary, postfix):
#     timestamp = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
#     projectname = "Cflow Playwright Automation"
#     modulename = "Admin Module - Add User"
#     tester = "Dinesh Aravinth ⚡"
#     browser = "Chromium"
#     region = "TEST"
#
#     html_block = f"""
#     <div style="
#         background: #ffffff;
#         padding: 12px 18px;
#         font-family: Verdana, sans-serif;
#         font-size: 16px;
#         font-weight: 600;
#         color: #000000;
#         border: 1px solid #ccc;
#         border-radius: 6px;
#         margin-top: 10px;">
#         📄 <strong>Project:</strong> {projectname} &nbsp;&nbsp; |
#         📁 <strong>Module:</strong> {modulename} &nbsp;&nbsp; |
#         👤 <strong>Tester:</strong> {tester} &nbsp;&nbsp; |
#         🌐 <strong>Browser:</strong> {browser} &nbsp;&nbsp; |
#         🌍 <strong>Region:</strong> {region} &nbsp;&nbsp; |
#         ⏰ <strong>Execution:</strong> {timestamp}
#     </div>
#     <br>
#     """
#
#     # Add safely as HTML extra (always string, never dict)
#     prefix.append(extras.html(html_block))

# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()
#     extra = getattr(report, 'extra', [])
#
#     if report.when == 'call' and report.failed:
#         try:
#             page = item.funcargs.get("page", None)
#             if page:
#                 screenshot_path = os.path.join("Reports", f"{item.name}.png")
#                 page.screenshot(path=screenshot_path)
#                 extra.append(extras.image(screenshot_path))
#         except Exception as e:
#             print(f"⚠️ Screenshot capture failed: {e}")
#
#     report.extra = extra
#
# @pytest.mark.optionalhook
# def pytest_html_results_summary(prefix, summary, postfix):
#     from datetime import datetime
#     timestamp = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
#
#     total = summary.passed + summary.failed + summary.skipped
#     passed = summary.passed
#     failed = summary.failed
#     skipped = summary.skipped
#
#     chart_html = f"""
#     <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
#     <canvas id="resultChart" width="400" height="150"></canvas>
#     <script>
#     var ctx = document.getElementById('resultChart').getContext('2d');
#     var chart = new Chart(ctx, {{
#         type: 'pie',
#         data: {{
#             labels: ['Passed', 'Failed', 'Skipped'],
#             datasets: [{{
#                 data: [{passed}, {failed}, {skipped}]
#             }}]
#         }},
#         options: {{
#             responsive: true,
#             plugins: {{
#                 legend: {{
#                     position: 'bottom'
#                 }}
#             }}
#         }}
#     }});
#     </script>
#     """
#
#     prefix.append(extras.html(chart_html))
#


# ------------------------------
# Track Test Session Start Time
# ------------------------------
@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    terminal_reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    if terminal_reporter and not hasattr(terminal_reporter, "_sessionstarttime"):
        terminal_reporter._sessionstarttime = datetime.now().timestamp()


# ------------------------------
# Remove Environment Section After Report Creation
# ------------------------------
def pytest_sessionfinish(session, exitstatus):
    report_path = getattr(session.config.option, "htmlpath", None)
    if report_path and os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        cleaned_html = re.sub(
            r"<h2>Environment</h2>.*?<table>.*?</table>",
            "",
            html_content,
            flags=re.S
        )

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(cleaned_html)

    print(f"\n✨ Test session finished. Exit status: {exitstatus}")

