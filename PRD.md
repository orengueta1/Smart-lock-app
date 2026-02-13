# Product Requirements Document: Smart-Clock AI 🕒

## 1. Project Overview
**Smart-Clock AI** is a simplified attendance and salary tracking application. Its core innovation is an "AI-First" entry system that allows users to describe their work hours in natural language, which the system then parses into structured data.

## 2. Target Audience
University students, freelancers, and shift-based employees who want a frictionless way to track their earnings without manual spreadsheets.

## 3. User Stories
* **As a user**, I want to type "I worked 9am to 6pm" and see my hours recorded automatically.
* **As a user**, I want to see my total earnings for the month update instantly.
* **As a user**, I want to be able to manually correct any entries if the AI makes a mistake.
* **As a user**, I want my data to be saved even if I refresh the page.

## 4. Functional Requirements

### A. AI Input Module (The "Smart" Part)
- **Input:** A text field for natural language input.
- **Processing:** Use an LLM to extract `Date` (default to today if not mentioned), `Start_Time`, and `End_Time`.
- **Output:** A JSON object used to populate the entry form.

### B. Attendance Dashboard
- **Manual Overrides:** Users can manually select Date, Start Time, and End Time using standard UI widgets.
- **Hourly Rate:** A numeric input field to set the wage (default: ₪50/hour).
- **Summary Statistics:** - Total Hours Worked (Monthly)
    - Total Estimated Salary (Monthly)

### C. Data Management
- **Persistence:** All logs must be saved to a local `attendance_log.csv` file.
- **Table View:** A sortable table displaying all recorded shifts.
- **Delete Function:** A button to remove specific entries from the log.

## 5. User Interface (UI) Design
- **Layout:** A clean, single-page Streamlit application.
- **Top Section:** Header and "AI Quick-Log" text area.
- **Middle Section:** Manual entry form (sidebar or center) and "Save" button.
- **Bottom Section:** KPIs (Total Pay) and the Data Table.

## 6. Technical Stack
- **Frontend/Backend:** Python (Streamlit).
- **AI Logic:** OpenAI API (GPT-4o/Claude) via Prompt Engineering.
- **Storage:** CSV (Local File).

## 7. Success Criteria
- The app successfully converts "Worked 8 to 4" into an 8-hour entry.
- The total salary calculates correctly (Hours * Rate).
- The data persists after the app is closed and reopened.