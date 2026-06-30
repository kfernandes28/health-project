# Life OS Health Dashboard

A personal health analytics dashboard built in Python to visualise blood biomarker trends over time.

## Overview

This project tracks blood test results over time and transforms raw laboratory data into an interactive dashboard.

The aim is to make long-term health trends easier to understand, monitor and compare.

It forms part of a larger "Life OS" ecosystem alongside the Finance Dashboard and Journal Dashboard.

---

## Features

- Import raw blood test results
- Canonical data processing pipeline
- Interactive HTML dashboard
- Biomarker trend visualisation
- Reference range comparison
- Longitudinal health tracking

---

## Project Structure

```
Health Project/
├── Baseline/
├── Config/
├── Milestones/
├── Scripts/
├── Stage 0 - Raw/
├── Stage 1 - Canonical/
├── Stage 2 - Dashboard/
```

---

## How to Run

1. Clone the repository

```bash
git clone <repo-url>
cd health-project
```

2. Create a virtual environment

```bash
python3 -m venv venv
```

3. Activate it

macOS / Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

5. Build the canonical dataset

```bash
python Scripts/build_canonical.py
```

6. Build the dashboard

```bash
python Scripts/build_dashboard.py
```

7. Open the generated HTML dashboard in your browser.

---

## Screenshots

Project screenshots will be added here.

---

## Future Improvements

- Single entry-point pipeline
- Public sample dataset
- Improved dashboard visualisations
- Database backend
- REST API
- Docker support
- CI/CD pipeline