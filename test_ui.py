"""Lab 5: automate login, create a task, mark it complete, log out.

Fill in pages/task_page.py first (it has TODO markers), then write the
four test functions below.

Run with:
    pytest test_ui.py -v --html=report.html --self-contained-html

DEMO_USERNAME = "demo"
DEMO_PASSWORD = "demo1234"
"""
from pages.login_page import LoginPage
from pages.task_page import NewTaskPage, TaskListPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEMO_USERNAME = "demo"
DEMO_PASSWORD = "demo1234"


def test_login_with_valid_credentials(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.open()
    login_page.login(DEMO_USERNAME, DEMO_PASSWORD)
    # TODO: wait for something on the next page that proves login
    # worked (the new-task form, or the page title). Assert on it.
    new_task_page = NewTaskPage(driver, base_url)
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            new_task_page.TITLE_INPUT
        )
    )
    assert driver.current_url.rstrip("/") == base_url.rstrip("/")


def test_login_with_invalid_credentials(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.open()
    login_page.login("demo", "wrong-password")
    error = login_page.wait_for_error()
    assert "Invalid username or password" in error.text


def test_create_task(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.open()
    login_page.login(DEMO_USERNAME, DEMO_PASSWORD)

    # TODO: use NewTaskPage to create a task with:
    #   title="Prepare slides", priority="2",
    #   due_date="2026-12-01", hours="3"
    # TODO: wait for the success banner and assert it is shown
    new_task_page = NewTaskPage(driver, base_url)
    new_task_page.open()

    new_task_page.create_task(
        title="Prepare slides",
        priority="2",
        due_date="2026-12-01",
        hours="3"
    )

    success_banner = new_task_page.wait_for_success()
    assert success_banner.is_displayed()



def test_mark_task_complete_and_logout(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.open()
    login_page.login(DEMO_USERNAME, DEMO_PASSWORD)

    new_task_page = NewTaskPage(driver, base_url)
    new_task_page.open()

    # Create a task with a unique name.
    import uuid
    unique_title = f"Task to complete {uuid.uuid4().hex[:8]}"

    new_task_page.create_task(
        title=unique_title,
        priority="2",
        due_date="2026-12-01",
        hours="3"
    )
    new_task_page.wait_for_success()

    # Open the task list.
    task_list_page = TaskListPage(driver, base_url)
    task_list_page.open()

    # Find the task created by this test.
    task_row = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                f"//tr[td[normalize-space()='{unique_title}']]"
            )
        )
    )

    # Extract the task ID from the row's ID.
    task_id = task_row.get_attribute("id").replace("task-row-", "")

    # Mark the newly created task as completed.
    task_list_page.mark_complete(task_id)

    # Wait until the task status becomes Completed.
    completed = task_list_page.wait_until_completed(task_id)
    assert completed is True

    # Log out.
    driver.find_element(By.ID, "logout-link").click()

    # Confirm that the login page appears.
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            (By.ID, "username")
        )
    )
    assert "/login" in driver.current_url
