"""
Pytest Configuration and Fixtures
Contains setup and teardown methods for tests
"""
import pytest
from utilities.driver_factory import DriverFactory


@pytest.fixture(scope='function')
def setup(request):
    """
    Setup fixture - initializes driver before each test
    
    Usage:
        @pytest.mark.platform('android')
        def test_example(setup):
            driver = setup
    """
    # Get platform from marker, default to 'android'
    marker = request.node.get_closest_marker('platform')
    platform = marker.args[0] if marker else 'android'
    
    # Initialize driver
    driver_factory = DriverFactory()
    driver = driver_factory.get_driver(platform)
    
    # Yield driver to test
    yield driver
    
    # Teardown - quit driver after test
    driver_factory.quit_driver()


@pytest.fixture(scope='function')
def android_driver(request):
    """Android driver fixture"""
    driver_factory = DriverFactory()
    driver = driver_factory.get_driver('android')
    yield driver
    driver_factory.quit_driver()


@pytest.fixture(scope='function')
def ios_driver(request):
    """iOS driver fixture"""
    driver_factory = DriverFactory()
    driver = driver_factory.get_driver('ios')
    yield driver
    driver_factory.quit_driver()


def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "platform(name): specify platform (android/ios)")
    config.addinivalue_line("markers", "login: mark test as login related")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshot on failure
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == 'call' and report.failed:
        # Test failed - capture screenshot
        driver = None
        if 'setup' in item.funcargs:
            driver = item.funcargs['setup']
        elif 'android_driver' in item.funcargs:
            driver = item.funcargs['android_driver']
        elif 'ios_driver' in item.funcargs:
            driver = item.funcargs['ios_driver']
        
        if driver:
            try:
                from utilities.common_utils import CommonUtils
                utils = CommonUtils(driver)
                screenshot_path = utils.take_screenshot(f"failed_{item.name}")
                print(f"\nScreenshot saved: {screenshot_path}")
            except Exception as e:
                print(f"\nFailed to capture screenshot: {str(e)}")
