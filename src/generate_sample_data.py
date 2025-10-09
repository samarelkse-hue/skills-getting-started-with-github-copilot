"""
Script to generate sample Excel and CSV files for star schema demonstration
"""

import pandas as pd
from pathlib import Path

# Create data directory
data_dir = Path(__file__).parent / "data"
data_dir.mkdir(exist_ok=True)

# Sample Students Data
students_data = {
    'email': [
        'michael@mergington.edu',
        'daniel@mergington.edu',
        'emma@mergington.edu',
        'sophia@mergington.edu',
        'john@mergington.edu',
        'olivia@mergington.edu',
        'alice@mergington.edu',
        'bob@mergington.edu'
    ],
    'name': [
        'Michael Johnson',
        'Daniel Smith',
        'Emma Williams',
        'Sophia Brown',
        'John Davis',
        'Olivia Miller',
        'Alice Wilson',
        'Bob Anderson'
    ],
    'grade_level': [9, 10, 11, 12, 9, 10, 11, 12]
}

# Sample Activities Data
activities_data = {
    'activity_name': [
        'Chess Club',
        'Programming Class',
        'Gym Class',
        'Art Club',
        'Music Band'
    ],
    'description': [
        'Learn strategies and compete in chess tournaments',
        'Learn programming fundamentals and build software projects',
        'Physical education and sports activities',
        'Explore creativity through various art mediums',
        'Learn and perform with musical instruments'
    ],
    'schedule': [
        'Fridays, 3:30 PM - 5:00 PM',
        'Tuesdays and Thursdays, 3:30 PM - 4:30 PM',
        'Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM',
        'Thursdays, 3:30 PM - 5:00 PM',
        'Mondays and Wednesdays, 4:00 PM - 5:30 PM'
    ],
    'max_participants': [12, 20, 30, 15, 25]
}

# Sample Signups Data
signups_data = {
    'student_email': [
        'michael@mergington.edu',
        'daniel@mergington.edu',
        'emma@mergington.edu',
        'sophia@mergington.edu',
        'john@mergington.edu',
        'olivia@mergington.edu',
        'alice@mergington.edu',
        'bob@mergington.edu',
        'michael@mergington.edu',
        'emma@mergington.edu'
    ],
    'activity_name': [
        'Chess Club',
        'Chess Club',
        'Programming Class',
        'Programming Class',
        'Gym Class',
        'Gym Class',
        'Art Club',
        'Music Band',
        'Programming Class',
        'Art Club'
    ],
    'signup_date': [
        '2024-01-15',
        '2024-01-16',
        '2024-01-15',
        '2024-01-17',
        '2024-01-18',
        '2024-01-18',
        '2024-01-19',
        '2024-01-20',
        '2024-01-21',
        '2024-01-22'
    ]
}

# Create DataFrames
df_students = pd.DataFrame(students_data)
df_activities = pd.DataFrame(activities_data)
df_signups = pd.DataFrame(signups_data)

# Save to Excel (multi-sheet workbook)
excel_file = data_dir / "school_activities.xlsx"
with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    df_students.to_excel(writer, sheet_name='Students', index=False)
    df_activities.to_excel(writer, sheet_name='Activities', index=False)
    df_signups.to_excel(writer, sheet_name='Signups', index=False)

print(f"Created Excel file: {excel_file}")

# Save to CSV files
csv_students = data_dir / "students.csv"
csv_activities = data_dir / "activities.csv"
csv_signups = data_dir / "signups.csv"

df_students.to_csv(csv_students, index=False)
df_activities.to_csv(csv_activities, index=False)
df_signups.to_csv(csv_signups, index=False)

print(f"Created CSV files:")
print(f"  - {csv_students}")
print(f"  - {csv_activities}")
print(f"  - {csv_signups}")
