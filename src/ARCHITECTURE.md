# Star Schema Architecture

## Schema Diagram

```
                            ┌──────────────────────┐
                            │   dim_students       │
                            ├──────────────────────┤
                            │ student_id (PK)      │
                     ┌──────│ email                │
                     │      │ name                 │
                     │      │ grade_level          │
                     │      └──────────────────────┘
                     │
                     │
                     │      ┌──────────────────────┐
                     │      │   dim_activities     │
                     │      ├──────────────────────┤
                     │      │ activity_id (PK)     │
                     │  ┌───│ activity_name        │
                     │  │   │ description          │
                     │  │   │ schedule             │
                     │  │   │ max_participants     │
                     │  │   └──────────────────────┘
                     │  │
                     │  │
    ┌────────────────┴──┴───────────────┐
    │     fact_activity_signups         │
    │    (CENTRAL FACT TABLE)           │
    ├───────────────────────────────────┤
    │ fact_signup_id (PK)               │
    │ student_id (FK) ──────────────────┘
    │ activity_id (FK) ─────────────────┘
    │ date_id (FK) ─────────────────────┐
    │ signup_timestamp                  │
    └───────────────────────────────────┘
                     │
                     │
                     │      ┌──────────────────────┐
                     │      │   dim_date           │
                     │      ├──────────────────────┤
                     │      │ date_id (PK)         │
                     └──────│ date                 │
                            │ day                  │
                            │ month                │
                            │ year                 │
                            │ weekday              │
                            └──────────────────────┘

Legend:
  PK = Primary Key
  FK = Foreign Key
```

## Data Flow

```
Excel/CSV Files
      │
      ▼
┌─────────────┐
│ Excel       │
│ Loader      │
└─────┬───────┘
      │
      ▼
┌─────────────────────────────────────┐
│  Star Schema Model                  │
│  ┌─────────────────────────────┐   │
│  │ Dimension Tables            │   │
│  │  • Students                 │   │
│  │  • Activities               │   │
│  │  • Dates                    │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ Fact Table                  │   │
│  │  • Activity Signups         │   │
│  └─────────────────────────────┘   │
└──────────────┬──────────────────────┘
               │
               ▼
        ┌──────────────┐
        │ FastAPI      │
        │ Endpoints    │
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │ Analytics    │
        │ & Reports    │
        └──────────────┘
```

## Example Queries

### Query 1: Activity Participation by Grade Level

```python
# Get all signups
signups = star_schema.fact_signups.values()

# Join with dimensions
for signup in signups:
    student = star_schema.dim_students[signup.student_id]
    activity = star_schema.dim_activities[signup.activity_id]
    print(f"Grade {student.grade_level} → {activity.activity_name}")
```

**Result:**
```
Grade 9 → Chess Club
Grade 10 → Chess Club
Grade 11 → Programming Class
Grade 12 → Programming Class
...
```

### Query 2: Monthly Signup Trends

```python
# Get all signups with dates
signups = star_schema.fact_signups.values()

# Group by month
monthly_counts = {}
for signup in signups:
    date = star_schema.dim_dates[signup.date_id]
    key = f"{date.year}-{date.month:02d}"
    monthly_counts[key] = monthly_counts.get(key, 0) + 1

print(monthly_counts)
```

**Result:**
```python
{
    "2024-01": 10,
    "2024-02": 15,
    ...
}
```

### Query 3: Popular Activities

```python
# Get activity analytics
analytics = star_schema.get_activity_analytics()

# Sort by signup count
sorted_activities = sorted(
    analytics,
    key=lambda x: x['current_signups'],
    reverse=True
)

for activity in sorted_activities:
    print(f"{activity['activity_name']}: {activity['current_signups']} signups")
```

**Result:**
```
Programming Class: 3 signups
Chess Club: 2 signups
Gym Class: 2 signups
Art Club: 2 signups
Music Band: 1 signups
```

## Why Star Schema?

### Advantages

1. **Simple Structure**
   - Easy to understand
   - Mirrors business concepts
   - Intuitive for non-technical users

2. **Query Performance**
   - Fewer joins required
   - Optimized for read operations
   - Fast aggregation queries

3. **Scalability**
   - Can handle large datasets
   - Easy to add new dimensions
   - Historical data tracking

4. **Flexibility**
   - Easy to extend
   - Supports ad-hoc queries
   - Works with BI tools

### Use Cases

- **Student Analytics**: Track participation patterns
- **Resource Planning**: Forecast activity capacity needs
- **Trend Analysis**: Identify popular activities over time
- **Grade-Level Reports**: Compare participation by grade
- **Capacity Management**: Monitor activity enrollment

## Extending the Schema

### Adding a New Dimension

To add a new dimension (e.g., Teachers):

1. Define the dimension model in `star_schema.py`:
```python
class DimTeacher(BaseModel):
    teacher_id: int
    name: str
    department: str
```

2. Add to StarSchemaModel:
```python
self.dim_teachers: Dict[int, DimTeacher] = {}
```

3. Update fact table to include teacher_id:
```python
class FactActivitySignup(BaseModel):
    teacher_id: int  # New field
    ...
```

4. Update Excel loader to load teacher data

### Adding a New Fact

To add a new fact (e.g., Activity Sessions):

1. Define the fact model:
```python
class FactActivitySession(BaseModel):
    session_id: int
    activity_id: int
    date_id: int
    teacher_id: int
    attendance_count: int
```

2. Add to StarSchemaModel:
```python
self.fact_sessions: Dict[int, FactActivitySession] = {}
```

3. Implement methods to add and query sessions
