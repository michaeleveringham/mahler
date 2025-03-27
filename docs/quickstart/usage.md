# Usage

Let's launch a browser, visit a site, and click the first link on the page.

```python
from mahler import Controller


controller = Controller(
    "playwright",
    "chrome",
    headless=False,
)
controller.goto("https://example.com")
link = controller.query_selector_all("a")
link.click()
```

Nice! Now let's change 1 line of code to do it in a different automation suite.

```python
from mahler import Controller

controller = Controller(
    "selenium",  # Changed
    "chrome",
    headless=False,
)
controller.goto("https://example.com")
link = controller.query_selector_all("a")
link.click()
```

A slightly more involved example. Let's login to a website! (Don't worry, these aren't real credentials.)

```python
from mahler import Controller

controller = Controller(
    "selenium",
    "firefox",
    headless=False,
)
controller.goto("https://www.scrapethissite.com/login/")
email_field = controller.query_selector("input#email")
email_field.type_on("jeanluc@ufop.org")
password_field = controller.query_selector("//input[@id='password']")
password_field.type_on("makeitso", delay=0.05)
login_button = controller.query_selector("input[type='submit']")
login_button.click()
```

Let's change 2 arguments to do it in a different automation suite with
a different browser type.

```python
from mahler import Controller

controller = Controller(
    "playwright",  # Changed
    "chrome",  # Changed
    headless=False,
)
controller.goto("https://www.scrapethissite.com/login/")
email_field = controller.query_selector("input#email")
email_field.type_on("jeanluc@ufop.org")
password_field = controller.query_selector("//input[@id='password']")
password_field.type_on("makeitso", delay=0.05)
login_button = controller.query_selector("input[type='submit']")
login_button.click()
```
