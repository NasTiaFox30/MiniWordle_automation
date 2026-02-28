# Mini Wordle Automation Tests 

This repository contains an automated test suite for the **Mini Wordle** Android application. 
All tests are written in **Python** using **Appium** + **Pytest**.

#### 📊 Test Cases
1. Victory Scenario: Verifies that entering "TEST" results in a win.
2. Game Over: Checks if the app blocks input after 6 failed attempts.
3. Duplicate Letters: Validates the color logic for repeated characters (e.g., "TEES").
4. Input Validation: Ensures the app rejects words shorter than 4 letters.


## 🛠 Instructions:
Before running the tests, ensure you have:
1. **[Node.js + npm:](https://nodejs.org/en/download/current)**
```bash
node -v 
npm -v
```
2. **[Appium Server 2.+](https://appium.io/docs/en/latest/quickstart/install/)**
```bash
npm install -g appium
```
3. Appium uiautomator2 (driver):
```bash
appium driver list
appium driver install uiautomator2 
```
4. **[Android Emulator (Adroid Studio recomended)](https://developer.android.com/studio)** (Android 11+).
5. **Python 3.10+**.
6. Get the Application
Download the latest `MiniWordle.apk` from the official **[App Releases](https://github.com/NasTiaFox30/MiniWordle/releases)** and place it into the `/app` folder of this project.
7. Create Environment + Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
OR
```
Ctrl + Shift + P
Python: Create Environment > Venv > Python version
```
8. Run Tests
Ensure your emulator (for example AdroidStudio) is running and Appium server is started, then execute in other terminal:
```bash
pytest tests/test_app.py
```


---------------------------------------------------------------
_**Creator: Anastasiia Bzova 2026**_ 