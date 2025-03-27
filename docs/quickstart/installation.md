# Installation

Install from PyPI.

```pip install mahler```

## Browser Management

Mahler tries to make browser management easy. When running Selenium browsers,
[`webdriver_manager`](https://github.com/SergeyPirogov/webdriver_manager) is used to
automatically download the needed drivers.

For Playwright, Mahler will run `playwright install` before launching the browser.
