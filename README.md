# 🎵 mahler

![PyPI - Version](https://img.shields.io/pypi/v/mahler)


Web browser automation wrapper.

## About

`mahler` is a web browser automation wrapper that offers a standard API regardless
of what automation suite is being used.

This allows for swapping between automation solutions (playwright, selenium)
without having to rewrite the actual browser control code.

`mahler` is named after [Gustav Mahler](https://en.wikipedia.org/wiki/Gustav_Mahler),
a 19th century composer that wrote some [sweet bass solos](https://www.youtube.com/watch?v=JEP2pA6srnk).

## Documentation

See the full [documentation](https://mahler.readthedocs.io/en/latest/index.html).

## Quickstart

Run `pip install mahler` to install package.

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

## To Do

- Expand fingerprint dataclass and usage to capture and apply full browser fingerprint.
- Add some blackbox functional tests for browser engines.
- Async browser support. Selenium doesn't have a native async implementation and [`selenium-async`](https://github.com/munro/python-selenium-async)
is no longer maintained.
- Support request interception. [`selenium-wire`](https://github.com/wkeeling/selenium-wire) is no longer maintained.
- Support [mokr](https://github.com/michaeleveringham/mokr) when it is fully released.
