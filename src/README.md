# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

**New Feature**: Now includes a **Star Schema data model** for analytics and Excel data integration! See [STAR_SCHEMA.md](STAR_SCHEMA.md) for details.

## Features

- View all available extracurricular activities
- Sign up for activities
- **Star Schema data model** for advanced analytics
- **Load data from Excel files** for easy data import
- **Analytics endpoints** for activity and student participation insights

## Getting Started

1. Install the dependencies:

   ```
   pip install -r ../requirements.txt
   ```
   
   Or manually:
   
   ```
   pip install fastapi uvicorn pandas openpyxl
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

### Original Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |

### Star Schema Analytics Endpoints

| Method | Endpoint                                | Description                                    |
| ------ | --------------------------------------- | ---------------------------------------------- |
| GET    | `/star-schema/analytics/activities`     | Get activity participation analytics           |
| GET    | `/star-schema/analytics/students`       | Get student participation analytics            |
| GET    | `/star-schema/dimensions/students`      | Get all students from dimension table          |
| GET    | `/star-schema/dimensions/activities`    | Get all activities from dimension table        |
| GET    | `/star-schema/dimensions/dates`         | Get all dates from dimension table             |
| GET    | `/star-schema/facts/signups`            | Get all signup facts                           |
| GET    | `/star-schema/student/{email}`          | Get student details with signups               |
| GET    | `/star-schema/activity/{activity_name}` | Get activity details with signups              |
| POST   | `/star-schema/load-excel`               | Upload and load data from Excel file           |

For detailed information about the Star Schema model, see [STAR_SCHEMA.md](STAR_SCHEMA.md).

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.
