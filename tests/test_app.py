import pytest
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Ścieżka do pliku APK
apk_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app", "MiniWordle.apk"))

@pytest.fixture
def driver():
    """Konfiguracja drivera Appium (Appium driver setup)"""
    options = AppiumOptions()
    options.set_capability('platformName', 'Android')
    options.set_capability('automationName', 'UiAutomator2')
    options.set_capability('deviceName', 'emulator-5554')
    options.set_capability('app', apk_path)
    options.set_capability('appPackage', 'com.example.miniwordle')
    options.set_capability('appActivity', '.MainActivity')
    options.set_capability('noReset', False)

    driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
    yield driver
    driver.quit()

def test_victory_scenario(driver):
    """Weryfikacja scenariusza pełnego zwycięstwa (Victory scenario check)"""
    input_field = driver.find_element(AppiumBy.ID, "com.example.miniwordle:id/etGuess")
    input_field.send_keys("TEST")
    
    driver.find_element(AppiumBy.ID, "com.example.miniwordle:id/btnCheck").click()
    
    result = driver.find_element(AppiumBy.ID, "com.example.miniwordle:id/tvResult")
    assert result.text == "VICTORY!"
    
    # Sprawdzenie przycisków po wygranej (Checking buttons state)
    reset_btn = driver.find_element(AppiumBy.ID, "com.example.miniwordle:id/btnReset")
    check_btn = driver.find_element(AppiumBy.ID, "com.example.miniwordle:id/btnCheck")
    assert reset_btn.is_displayed()
    assert check_btn.get_attribute("enabled") == "false"

def test_game_over_scenario(driver):
    """Weryfikacja limitu prób i przegranej (Game Over and attempts limit check)"""
    input_field = driver.find_element(AppiumBy.ID, "com.example.miniwordle:id/etGuess")
    check_btn = driver.find_element(AppiumBy.ID, "com.example.miniwordle:id/btnCheck")
    
    # Wprowadzanie błędnego słowa 6 razy (Entering wrong word 6 times)
    for _ in range(6):
        input_field.send_keys("FAIL")
        check_btn.click()
    
    result = driver.find_element(AppiumBy.ID, "com.example.miniwordle:id/tvResult")
    assert "GAME OVER" in result.text
    
    attempts_text = driver.find_element(AppiumBy.ID, "com.example.miniwordle:id/tvAttempts").text
    assert "0" in attempts_text

def test_duplicate_letter_logic(driver):
    """Weryfikacja logiki powtarzających się liter (Duplicate letters logic check)"""
    input_field = driver.find_element(AppiumBy.ID, "com.example.miniwordle:id/etGuess")
    input_field.send_keys("TEES")
    driver.find_element(AppiumBy.ID, "com.example.miniwordle:id/btnCheck").click()

    # Sprawdzanie liter w historii (Checking letters in history container)
    history = driver.find_element(AppiumBy.ID, "com.example.miniwordle:id/historyContainer")
    first_row = history.find_element(AppiumBy.CLASS_NAME, "android.widget.LinearLayout")
    boxes = first_row.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
    
    assert boxes[0].text == "T"
    assert boxes[1].text == "E"
    assert boxes[2].text == "E"
    assert boxes[3].text == "S"
    assert len(boxes) == 4

def test_short_word_validation(driver):
    """Weryfikacja walidacji zbyt krótkiego słowa (Short word validation check)"""
    initial_attempts = driver.find_element(AppiumBy.ID, "com.example.miniwordle:id/tvAttempts").text
    
    input_field = driver.find_element(AppiumBy.ID, "com.example.miniwordle:id/etGuess")
    input_field.send_keys("ABC")
    driver.find_element(AppiumBy.ID, "com.example.miniwordle:id/btnCheck").click()
    
    # Sprawdzenie komunikatu o błędzie (Checking error message)
    result = driver.find_element(AppiumBy.ID, "com.example.miniwordle:id/tvResult")
    assert result.text == "Must be 4 letters!"
    
    # Weryfikacja czy licznik prób nie zmienił się (Checking if attempts count remains same)
    current_attempts = driver.find_element(AppiumBy.ID, "com.example.miniwordle:id/tvAttempts").text
    assert initial_attempts == current_attempts