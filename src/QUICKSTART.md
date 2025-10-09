# Star Schema Quick Start Guide

## What is a Star Schema?

A star schema is a database design pattern commonly used in data warehousing and business intelligence. It organizes data into:
- **Fact tables**: Store measurable events (e.g., signups)
- **Dimension tables**: Store descriptive attributes (e.g., students, activities, dates)

This structure makes it easy to analyze data and answer business questions like:
- "How many students signed up for each activity?"
- "Which activities are most popular?"
- "What is the participation rate by grade level?"

## Quick Start

### 1. Generate Sample Data

```bash
cd src
python generate_sample_data.py
```

This creates sample Excel and CSV files in `src/data/`.

### 2. Run the Test Script

```bash
cd src
python test_star_schema.py
```

This validates the star schema implementation and shows example queries.

### 3. Start the API Server

```bash
cd src
python -m uvicorn app:app --reload
```

Then visit:
- API documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Using the API

### Get Activity Analytics

```bash
curl http://localhost:8000/star-schema/analytics/activities
```

**Response:**
```json
[
  {
    "activity_name": "Chess Club",
    "description": "Learn strategies and compete in chess tournaments",
    "schedule": "Fridays, 3:30 PM - 5:00 PM",
    "max_participants": 12,
    "current_signups": 2,
    "spots_left": 10
  }
]
```

### Get Student Details

```bash
curl http://localhost:8000/star-schema/student/michael@mergington.edu
```

**Response:**
```json
{
  "student": {
    "student_id": 1,
    "email": "michael@mergington.edu",
    "name": "Michael Johnson",
    "grade_level": 9
  },
  "signups": [
    {
      "activity_name": "Chess Club",
      "signup_date": "2024-01-15",
      "signup_timestamp": "2024-01-15T00:00:00"
    }
  ]
}
```

### Upload Excel Data

```bash
curl -X POST "http://localhost:8000/star-schema/load-excel" \
  -F "file=@data/school_activities.xlsx"
```

## Excel File Format

Your Excel file should have three sheets:

### Students Sheet
| email | name | grade_level |
|-------|------|-------------|
| john@school.edu | John Doe | 10 |
| jane@school.edu | Jane Smith | 11 |

### Activities Sheet
| activity_name | description | schedule | max_participants |
|--------------|-------------|----------|-----------------|
| Chess Club | Chess tournaments | Fridays 3-5 PM | 12 |
| Art Club | Creative arts | Thursdays 3-5 PM | 15 |

### Signups Sheet
| student_email | activity_name | signup_date |
|--------------|---------------|-------------|
| john@school.edu | Chess Club | 2024-01-15 |
| jane@school.edu | Art Club | 2024-01-16 |

## Using in Python

```python
from star_schema import StarSchemaModel
from excel_loader import ExcelDataLoader

# Create star schema
schema = StarSchemaModel()
loader = ExcelDataLoader(schema)

# Load data
results = loader.load_all_from_excel("data/school_activities.xlsx")
print(f"Loaded: {results}")

# Query analytics
activities = schema.get_activity_analytics()
for activity in activities:
    print(f"{activity['activity_name']}: {activity['current_signups']} signups")

# Query by student
signups = schema.get_signups_by_student("john@school.edu")
print(f"Student has {len(signups)} signups")
```

## Available API Endpoints

### Analytics
- `GET /star-schema/analytics/activities` - Activity participation stats
- `GET /star-schema/analytics/students` - Student participation stats

### Dimensions
- `GET /star-schema/dimensions/students` - All students
- `GET /star-schema/dimensions/activities` - All activities
- `GET /star-schema/dimensions/dates` - All dates

### Facts
- `GET /star-schema/facts/signups` - All signup events

### Queries
- `GET /star-schema/student/{email}` - Student details with signups
- `GET /star-schema/activity/{name}` - Activity details with signups

### Data Loading
- `POST /star-schema/load-excel` - Upload Excel file

## Benefits

1. **Easy to Understand**: Simple structure mirrors real-world concepts
2. **Fast Queries**: Optimized for analytical queries
3. **Scalable**: Can handle large amounts of data
4. **Flexible**: Easy to add new dimensions or facts
5. **Excel Integration**: Import data from Excel spreadsheets

## Next Steps

- See [STAR_SCHEMA.md](STAR_SCHEMA.md) for detailed documentation
- Customize the schema for your needs
- Add more dimensions (e.g., teachers, classrooms)
- Build reports and dashboards using the analytics endpoints
