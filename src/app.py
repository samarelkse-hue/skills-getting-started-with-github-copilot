"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.

Now includes a star schema data model for analytics and Excel data integration.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
import os
from pathlib import Path
from star_schema import star_schema
from excel_loader import ExcelDataLoader

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities with Star Schema analytics")

# Initialize Excel data loader
excel_loader = ExcelDataLoader(star_schema)

# Load sample data from Excel on startup
data_dir = Path(__file__).parent / "data"
excel_file = data_dir / "school_activities.xlsx"
if excel_file.exists():
    try:
        results = excel_loader.load_all_from_excel(str(excel_file))
        print(f"Loaded data from Excel: {results}")
    except Exception as e:
        print(f"Warning: Could not load Excel data: {e}")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    
    # Also add to star schema if student exists
    try:
        star_schema.add_signup(email, activity_name)
    except Exception as e:
        print(f"Warning: Could not add to star schema: {e}")
    
    return {"message": f"Signed up {email} for {activity_name}"}


# Star Schema Endpoints

@app.get("/star-schema/analytics/activities")
def get_activity_analytics():
    """Get analytics on activity signups from the star schema"""
    return star_schema.get_activity_analytics()


@app.get("/star-schema/analytics/students")
def get_student_analytics():
    """Get analytics on student participation from the star schema"""
    return star_schema.get_student_analytics()


@app.get("/star-schema/dimensions/students")
def get_all_students():
    """Get all students from the dimension table"""
    return [student.dict() for student in star_schema.dim_students.values()]


@app.get("/star-schema/dimensions/activities")
def get_all_activities_dim():
    """Get all activities from the dimension table"""
    return [activity.dict() for activity in star_schema.dim_activities.values()]


@app.get("/star-schema/dimensions/dates")
def get_all_dates():
    """Get all dates from the dimension table"""
    return [date.dict() for date in star_schema.dim_dates.values()]


@app.get("/star-schema/facts/signups")
def get_all_signups():
    """Get all signup facts from the fact table"""
    return [signup.dict() for signup in star_schema.fact_signups.values()]


@app.get("/star-schema/student/{email}")
def get_student_details(email: str):
    """Get student details and their signups"""
    student = star_schema.get_student_by_email(email)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    signups = star_schema.get_signups_by_student(email)
    
    # Enrich with activity details
    signup_details = []
    for signup in signups:
        activity = star_schema.dim_activities.get(signup.activity_id)
        date = star_schema.dim_dates.get(signup.date_id)
        signup_details.append({
            "activity_name": activity.activity_name if activity else "Unknown",
            "signup_date": date.date if date else "Unknown",
            "signup_timestamp": signup.signup_timestamp
        })
    
    return {
        "student": student.dict(),
        "signups": signup_details
    }


@app.get("/star-schema/activity/{activity_name}")
def get_activity_details(activity_name: str):
    """Get activity details and signups"""
    activity = star_schema.get_activity_by_name(activity_name)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    signups = star_schema.get_signups_by_activity(activity_name)
    
    # Enrich with student details
    signup_details = []
    for signup in signups:
        student = star_schema.dim_students.get(signup.student_id)
        date = star_schema.dim_dates.get(signup.date_id)
        signup_details.append({
            "student_name": student.name if student else "Unknown",
            "student_email": student.email if student else "Unknown",
            "grade_level": student.grade_level if student else "Unknown",
            "signup_date": date.date if date else "Unknown",
            "signup_timestamp": signup.signup_timestamp
        })
    
    return {
        "activity": activity.dict(),
        "signups": signup_details,
        "total_signups": len(signup_details),
        "spots_left": activity.max_participants - len(signup_details)
    }


@app.post("/star-schema/load-excel")
async def load_excel_file(file: UploadFile = File(...)):
    """Upload and load data from an Excel file"""
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="File must be an Excel file (.xlsx or .xls)")
    
    # Save uploaded file temporarily
    temp_dir = Path("/tmp")
    temp_file = temp_dir / file.filename
    
    try:
        contents = await file.read()
        with open(temp_file, "wb") as f:
            f.write(contents)
        
        # Load data from the file
        results = excel_loader.load_all_from_excel(str(temp_file))
        
        # Clean up
        temp_file.unlink()
        
        return {"message": "Data loaded successfully", "results": results}
    except Exception as e:
        if temp_file.exists():
            temp_file.unlink()
        raise HTTPException(status_code=500, detail=f"Error loading Excel file: {str(e)}")

