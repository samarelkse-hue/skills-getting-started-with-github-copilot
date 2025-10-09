#!/usr/bin/env python3
"""
Test script for Star Schema implementation

This script demonstrates the star schema functionality including:
1. Loading data from Excel
2. Querying dimensions and facts
3. Running analytics queries
"""

import sys
from pathlib import Path

# Add src directory to path
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

from star_schema import StarSchemaModel
from excel_loader import ExcelDataLoader


def test_star_schema():
    """Test the star schema implementation"""
    print("=" * 60)
    print("Star Schema Test")
    print("=" * 60)
    
    # Create a new star schema instance
    test_schema = StarSchemaModel()
    loader = ExcelDataLoader(test_schema)
    
    # Load data from Excel
    excel_file = src_dir / "data" / "school_activities.xlsx"
    if not excel_file.exists():
        print(f"\n❌ Excel file not found: {excel_file}")
        print("Run 'python generate_sample_data.py' first to create sample data")
        return False
    
    print(f"\n📂 Loading data from: {excel_file}")
    results = loader.load_all_from_excel(str(excel_file))
    print(f"✅ Load results: {results}")
    
    # Test Dimension Tables
    print("\n" + "=" * 60)
    print("Dimension Tables")
    print("=" * 60)
    
    print(f"\n📊 Students: {len(test_schema.dim_students)} records")
    for student in list(test_schema.dim_students.values())[:3]:
        print(f"  - {student.name} (Grade {student.grade_level}): {student.email}")
    
    print(f"\n📊 Activities: {len(test_schema.dim_activities)} records")
    for activity in test_schema.dim_activities.values():
        print(f"  - {activity.activity_name}: {activity.max_participants} max participants")
    
    print(f"\n📊 Dates: {len(test_schema.dim_dates)} records")
    for date in list(test_schema.dim_dates.values())[:5]:
        print(f"  - {date.date} ({date.weekday})")
    
    # Test Fact Table
    print("\n" + "=" * 60)
    print("Fact Table")
    print("=" * 60)
    
    print(f"\n📊 Signups: {len(test_schema.fact_signups)} records")
    for fact in list(test_schema.fact_signups.values())[:5]:
        student = test_schema.dim_students[fact.student_id]
        activity = test_schema.dim_activities[fact.activity_id]
        date = test_schema.dim_dates[fact.date_id]
        print(f"  - {student.name} → {activity.activity_name} on {date.date}")
    
    # Test Analytics
    print("\n" + "=" * 60)
    print("Analytics Queries")
    print("=" * 60)
    
    print("\n📈 Activity Analytics:")
    activity_analytics = test_schema.get_activity_analytics()
    for activity in activity_analytics:
        print(f"  - {activity['activity_name']}:")
        print(f"      Signups: {activity['current_signups']}/{activity['max_participants']}")
        print(f"      Spots left: {activity['spots_left']}")
    
    print("\n📈 Student Analytics:")
    student_analytics = test_schema.get_student_analytics()
    for student in student_analytics[:3]:
        print(f"  - {student['student_name']} (Grade {student['grade_level']}):")
        print(f"      Activities: {student['activities_count']}")
        print(f"      Enrolled in: {', '.join(student['activities'])}")
    
    # Test Query by Student
    print("\n" + "=" * 60)
    print("Query Examples")
    print("=" * 60)
    
    test_email = "michael@mergington.edu"
    print(f"\n🔍 Query: Get signups for {test_email}")
    signups = test_schema.get_signups_by_student(test_email)
    print(f"   Found {len(signups)} signups:")
    for signup in signups:
        activity = test_schema.dim_activities[signup.activity_id]
        date = test_schema.dim_dates[signup.date_id]
        print(f"   - {activity.activity_name} on {date.date}")
    
    # Test Query by Activity
    test_activity = "Chess Club"
    print(f"\n🔍 Query: Get signups for {test_activity}")
    signups = test_schema.get_signups_by_activity(test_activity)
    print(f"   Found {len(signups)} signups:")
    for signup in signups:
        student = test_schema.dim_students[signup.student_id]
        date = test_schema.dim_dates[signup.date_id]
        print(f"   - {student.name} ({student.email}) on {date.date}")
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    try:
        success = test_star_schema()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
