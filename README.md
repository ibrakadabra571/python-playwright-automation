# Automated Testing Project

This project is designed for automated testing using Playwright and Pytest frameworks.

## Installing Dependencies

To get started, install the necessary dependencies by running command:

```sh
pip install -r requirements.txt
```

## Running Tests with Markers

You can run tests using markers with the `-m` flag. For example:

```sh
pytest -m alerts
```

For more details of running tests with Pytest, see [Running Tests with Pytest](https://docs.pytest.org/en/latest/how-to/usage.html).

## Running Tests with different options

To run tests with different configurations, such as specific browsers or in headless mode, use the `--browser` and `--headless` flags. By default, headless mode is disabled (False):

```sh
pytest --browser=firefox --headless
```

## Useful Links

- [Pytest Documentation](https://docs.pytest.org/en/latest/)
- [Running Tests with Pytest](https://docs.pytest.org/en/latest/how-to/usage.html)