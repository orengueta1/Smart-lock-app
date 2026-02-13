# 🍊 Smart-Clock AI

*> "Tracking your work hours has never been easier."*

**Smart-Clock AI** is a modern, AI-powered attendance and salary tracking application designed for students, freelancers, and shift-based employees. It simplifies the tedious process of logging work hours by allowing you to simply describe your shift in natural language.

---

## ✨ Features

### ⚡ AI Quick-Log
Forget manual date pickers. Just type like you speak:
> *"Worked yesterday from 9am to 5pm"*
> *"18/1/26 15:00-20:00"*

The intelligent parsing engine automatically extracts the date, start time, and end time to fill out the log for you.

### 📊 Real-Time Dashboard
*   **Track Earnings:** Instantly see your total estimated salary based on your hourly rate.
*   **Hours Worked:** Monitor your total hours for the month.
*   **Visual Metrics:** Clean, card-style metrics for quick insights.

### 📝 Flexible & Secure
*   **Manual Entry:** Full control to manually adjust or enter specific times.
*   **Data Persistence:** All your data is safely stored locally in `attendance_log.csv`.
*   **Management:** View your complete history and delete incorrect entries with ease.

---

## 🚀 Getting Started

### Prerequisites
*   Python 3.8 or higher

### Installation

1.  **Clone the repository** (or download the files):
    ```bash
    git clone https://github.com/yourusername/smart-clock-ai.git
    cd smart-clock-ai
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Running the App

**Option 1: The Easy Way (Windows)**
Double-click the `run_app.bat` file.

**Option 2: via Command Line**
```bash
python -m streamlit run app.py
```

The application will launch automatically in your default web browser at `http://localhost:8501`.

---

## 🛠️ Technologies Used

*   **[Streamlit](https://streamlit.io/):** For the beautiful, responsive web interface.
*   **Pandas:** For robust data handling and storage.
*   **Python:** The core logic.

---

## 📂 Project Structure

*   `app.py`: The main application interface and logic.
*   `ai_parser.py`: The intelligence module handling natural language processing.
*   `data_manager.py`: Handles CSV storage, loading, and deletion.
*   `run_app.bat`: One-click launcher script.

---

## 📄 License

This project is open-source and available for personal and educational use.

---

*Created with ❤️ by Oreng*
