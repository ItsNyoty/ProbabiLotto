# ProbabiLotto - Premium Prediction Engine

ProbabiLotto is a tool designed to analyze historical lottery data and generate statistical predictions. It uses a hybrid model combining "Hot" (frequent) and "Cold" (overdue) number analysis to suggest potential combinations for various lottery games.

## Supported Games
- **Lotto (BE)**
- **Extra Lotto (BE)**
- **EuroMillions**
- **VikingLotto**
- **Joker+**
- **Pick3**
- **Keno**

## Features
- **Hybrid Prediction Model**: Balances frequently drawn numbers with overdue ones for a statistically diverse selection.
- **Historical Data Analysis**: Automatically filters data to ensure relevance (e.g., using only post-2011 data for Lotto).
- **Visual Insights**: Interactive charts showing number frequency distributions.
- **Smart Explanations**: Provides context on why specific numbers were chosen (e.g., "Top hot number", "Long overdue").
- **Special Game Support**: Handles unique game features like Joker+ constellations and EuroMillions stars.

## Installation & Usage

1.  **Install Dependencies**:
    ```bash
    pip install fastapi uvicorn pandas openpyxl
    ```

2.  **Run the Server**:
    ```bash
    python main.py
    ```

3.  **Open the Application**:
    Navigate to `http://localhost:8000` in your web browser.

## ⚠️ DISCLAIMER: PLEASE READ CAREFULLY

**ProbabiLotto is for entertainment and informational purposes only.**

*   **No Guarantees**: This tool uses statistical probability based on past events, but lottery draws are fundamentally random independent events. **This tool CANNOT and DOES NOT guarantee a win.**
*   **Not 100% Accurate**: There is no algorithm that can predict lottery numbers with 100% certainty. The "predictions" are merely statistical suggestions.
*   **Play Responsibly**: Never gamble with money you cannot afford to lose. If you or someone you know has a gambling problem, please seek help.

**By using this software, you acknowledge that the developers are not responsible for any financial losses incurred.**
