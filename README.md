# Lab 5: Web UI Automation (Selenium)

Testers (pair): GROUP 2 
1. Alya Nabihah bt Ahmad Kamarzaman (22012109)
2. Mohammad Syarafuddin Bin Mohd Zaidi (22006949)
3. ⁠Nurul Hafizhah Binti Zainal Abidin (22005732)
4. ⁠Muhammad Adam Muzir Bin Mohamad Azmi (22006801)

Date: 19/10/2026

**Duration:** 2 hours  **Work mode:** groups

**Application under test:** `https://pytodo-lab5.onrender.com` (a running PyTodo app with login)

## 1. What you are building

This project uses Selenium WebDriver and pytest to automate testing of a web-based task management application.

The automated tests open a browser, log in, create a task, mark a task as completed, and log out. The tests run automatically without requiring manual interaction with the browser.

The project uses the Page Object Model (POM) to separate page interactions from test cases and pytest-html to generate an HTML test report with screenshots.

Application under test: https://pytodo-lab5.onrender.com

## 2. Setup, step by step

**Step 1. Install Google Chrome**, if it is not already on your computer.
Download from google.com/chrome and install normally.

**Step 2. Install Python packages.** Open a terminal in this folder and run:

```bash
pip install -r requirements.txt
```

This installs `selenium`, `pytest`, and `pytest-html`. You do not need to
install a separate chromedriver file. Selenium 4.6 and later finds and
downloads the matching driver for your installed Chrome automatically, the
first time you run a test.

**Step 3. Confirm it works.** Run:

```bash
python -c "from selenium import webdriver; d = webdriver.Chrome(); d.get('https://example.com'); print(d.title); d.quit()"
```

A Chrome window should briefly open, visit example.com, and close. The
terminal should print `Example Domain`. If this fails, fix it before
continuing, nothing else in this lab will work until this line succeeds.

**Step 4. Set the app URL.** This repo's tests read the app address from
an environment variable. Set it once per terminal session:

```bash
export PYTODO_URL="https://pytodo-lab5.onrender.com"
```

On Windows PowerShell, use `$env:PYTODO_URL="https://pytodo-lab5.onrender.com"` instead.

**Step 5. Log in once by hand first.** Open `https://pytodo-lab5.onrender.com/login` in your own
browser, and check that logging in with username `demo` and password
`demo1234` works, and that you can create a task. This confirms the app
itself is reachable before you automate it.

## Project Structure

| File or directory | Purpose |
|---|---|
| `pages/login_page.py` | Contains the login page locators and methods for opening the login page, entering credentials, and checking login errors. |
| `pages/task_page.py` | Contains the page objects and methods for creating tasks, accessing the task list, and marking tasks as completed. |
| `pages/__init__.py` | Identifies `pages` as a Python package. |
| `test_ui.py` | Contains the automated Selenium test cases. |
| `conftest.py` | Configures pytest fixtures, the browser driver, the application URL, and test setup. |
| `requirements.txt` | Lists the Python dependencies required to run the project. |
| `report.html` | Generated HTML report containing test results and links to screenshots. |
| `screenshots/` | Contains screenshots captured during test execution. |
| `.gitignore` | Prevents generated files, Python caches, and unnecessary local files from being committed. |
| `README.md` | Provides project documentation, setup instructions, test execution steps, and submission details. |

## 6. Page Object Model (POM)

The Page Object Model separates web page interactions from the test logic.

Each page object defines the locators used to find web elements and methods that perform actions on those elements.

For example, LoginPage handles login-related actions, while NewTaskPage and TaskListPage handle task creation and task completion.

This structure improves readability, reusability, and maintainability. If a page locator changes, the relevant page object can be updated without unnecessarily rewriting every test case.

## 7. The rule for this lab: no time.sleep

A page does not always finish loading or updating the instant you click
something. Marking a task complete on this app takes about 0.7 seconds
to process, through a background JavaScript call. If your test uses
`time.sleep(1)` to wait for it, two things can go wrong: it is slower
than necessary when 0.7 seconds would do, and it can still fail if the
server is briefly slower than your guessed number.

The correct tool is `WebDriverWait`, already used in `login_page.py`:

```python
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "some-id"))
)
```

This waits up to 10 seconds, checking repeatedly, and moves on the
instant the condition is true. Do not write `time.sleep` anywhere in
`pages/task_page.py` or `test_ui.py`.

## 8. Your task

1. Open `pages/login_page.py` and read it fully. This is a complete,
   working example.
2. Open `pages/task_page.py`. Fill in every method marked `TODO`,
   following the same pattern as `login_page.py`.
3. Open `test_ui.py`. Fill in every section marked `TODO`.
4. Run your tests:

```bash
pytest test_ui.py -v --html=report.html --self-contained-html
```
| Test case | Purpose |
|---|---|
| `test_login_with_valid_credentials` | Verifies that a user can log in successfully using valid credentials. |
| `test_login_with_invalid_credentials` | Verifies that the application displays an appropriate error message when invalid credentials are entered. |
| `test_create_task` | Verifies that a new task can be created successfully and that the success banner appears. |
| `test_mark_task_complete_and_logout` | Creates a task with a unique title, identifies the correct task, marks it as completed, waits for the status to update to `Completed`, and verifies that logging out returns the user to the login page. |

5. Open `report.html` in a browser. Every test should show a screenshot.
   A passing test's last screenshot should show the completed state
   (success banner shown, or task marked Completed). A failing test's
   screenshot shows you where it broke.

## 9. Submit

Commit `pages/task_page.py`, `test_ui.py`, and `report.html` to your repo.

| Criterion | Points |
|---|---|
| Login test (valid and invalid credentials) | 20 |
| Create task test, waits for success banner correctly | 20 |
| Mark complete test, uses WebDriverWait, not time.sleep | 25 |
| Logout test, confirms return to login page | 15 |
| HTML report generated with screenshots for every test | 20 |
