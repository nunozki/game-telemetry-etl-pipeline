
# 🎮 Steam Telemetry ETL Pipeline

A robust, Object-Oriented Python ETL (Extract, Transform, Load) pipeline designed to fetch, clean, and store real-time player telemetry data from the public Steam API.

This project demonstrates core **Data Engineering** principles, bridging my background in game engine architecture with scalable data processing and analytics.

## 🏗️ Architecture & Pipeline Flow

The pipeline is orchestrated by `main.py` and is strictly divided into three isolated phases, following the Separation of Concerns principle:

1. **Extract (`extract.py`):** - Connects to the Steamworks Web API.

   - Utilizes `requests.Session()` for connection pooling and efficient batch requests.
   - Implements robust error handling (timeouts, HTTP errors, and connection drops) to ensure pipeline resilience.
2. **Transform (`transform.py`):** - Uses `pandas` to convert raw JSON/Dictionaries into structured DataFrames.

   - Enriches data by mapping numeric App IDs to human-readable game names (simulating a Dimension Table join).
   - Enforces Data Quality checks (handling missing values, standardizing datetime schemas, and ordering columns).
3. **Load (`load.py`):** - Uses native `sqlite3` and SQL DDL statements to ensure the target database schema exists (`IF NOT EXISTS`).

   - Inserts the transformed DataFrame into a relational SQLite database (`steam_telemetry.db`).
   - Runs a final SQL Data Query (DQL) to validate the integrity and accuracy of the load process.

## 🛠️ Tech Stack & Skills Demonstrated

* **Language:** Python 3.x
* **Data Processing:** Pandas
* **Database:** SQLite (SQL DDL & DQL)
* **API Integration:** `requests` (RESTful APIs)
* **Engineering Best Practices:** Object-Oriented Programming (OOP), Type Hinting, Context Managers (`with`), Guard Clauses, Fail-Fast mechanisms.

## 🚀 How to Run Locally

### 1. Clone the repository

```bash
git clone [https://github.com/nunozki/game-telemetry-etl-pipeline.git](https://github.com/nunozki/steam-telemetry-etl.git)
cd game-telemetry-etl-pipeline
```
