"""
Example: Complex analytical query using the Star Schema
This demonstrates how easy it is to answer business questions
"""
from star_schema import StarSchemaModel
from excel_loader import ExcelDataLoader

# Load data
schema = StarSchemaModel()
loader = ExcelDataLoader(schema)
loader.load_all_from_excel("data/school_activities.xlsx")

print("Business Question: What is the participation rate by grade level?")
print("=" * 70)

# Group signups by grade level
grade_participation = {}
for signup in schema.fact_signups.values():
    student = schema.dim_students[signup.student_id]
    grade = student.grade_level
    if grade not in grade_participation:
        grade_participation[grade] = {"students": set(), "signups": 0}
    grade_participation[grade]["students"].add(student.student_id)
    grade_participation[grade]["signups"] += 1

# Calculate and display
print("\nGrade Level | Unique Students | Total Signups | Avg Signups/Student")
print("-" * 70)
for grade in sorted(grade_participation.keys()):
    data = grade_participation[grade]
    unique = len(data["students"])
    total = data["signups"]
    avg = total / unique if unique > 0 else 0
    print(f"Grade {grade:2d}    | {unique:15d} | {total:13d} | {avg:19.2f}")

print("\nThis query was easy because:")
print("  ✓ Dimensions store student attributes (grade_level)")
print("  ✓ Facts store signup events")
print("  ✓ Foreign keys connect them efficiently")
