"""
Star Schema Model for Excel Data

This module implements a star schema data model for analyzing
student activity signups from Excel data sources.

Star Schema Design:
- Fact Table: activity_signups (fact_signup_id, student_id, activity_id, date_id, grade_level)
- Dimension Tables:
  * dim_students (student_id, email, name, grade_level)
  * dim_activities (activity_id, activity_name, description, schedule, max_participants)
  * dim_date (date_id, date, day, month, year, weekday)
"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel


# Dimension Models
class DimStudent(BaseModel):
    """Student dimension table"""
    student_id: int
    email: str
    name: str
    grade_level: int


class DimActivity(BaseModel):
    """Activity dimension table"""
    activity_id: int
    activity_name: str
    description: str
    schedule: str
    max_participants: int


class DimDate(BaseModel):
    """Date dimension table"""
    date_id: int
    date: str
    day: int
    month: int
    year: int
    weekday: str


# Fact Model
class FactActivitySignup(BaseModel):
    """Fact table for activity signups"""
    fact_signup_id: int
    student_id: int
    activity_id: int
    date_id: int
    signup_timestamp: str


class StarSchemaModel:
    """Star Schema data warehouse for activity signups"""
    
    def __init__(self):
        self.dim_students: Dict[int, DimStudent] = {}
        self.dim_activities: Dict[int, DimActivity] = {}
        self.dim_dates: Dict[int, DimDate] = {}
        self.fact_signups: Dict[int, FactActivitySignup] = {}
        
        # Auto-increment counters
        self._student_counter = 1
        self._activity_counter = 1
        self._date_counter = 1
        self._fact_counter = 1
        
        # Lookup indexes
        self._student_email_index: Dict[str, int] = {}
        self._activity_name_index: Dict[str, int] = {}
        self._date_string_index: Dict[str, int] = {}
    
    def add_student(self, email: str, name: str, grade_level: int) -> int:
        """Add a student to the dimension table"""
        if email in self._student_email_index:
            return self._student_email_index[email]
        
        student_id = self._student_counter
        student = DimStudent(
            student_id=student_id,
            email=email,
            name=name,
            grade_level=grade_level
        )
        self.dim_students[student_id] = student
        self._student_email_index[email] = student_id
        self._student_counter += 1
        return student_id
    
    def add_activity(self, activity_name: str, description: str, 
                    schedule: str, max_participants: int) -> int:
        """Add an activity to the dimension table"""
        if activity_name in self._activity_name_index:
            return self._activity_name_index[activity_name]
        
        activity_id = self._activity_counter
        activity = DimActivity(
            activity_id=activity_id,
            activity_name=activity_name,
            description=description,
            schedule=schedule,
            max_participants=max_participants
        )
        self.dim_activities[activity_id] = activity
        self._activity_name_index[activity_name] = activity_id
        self._activity_counter += 1
        return activity_id
    
    def add_date(self, date: datetime) -> int:
        """Add a date to the dimension table"""
        date_str = date.strftime("%Y-%m-%d")
        if date_str in self._date_string_index:
            return self._date_string_index[date_str]
        
        date_id = self._date_counter
        dim_date = DimDate(
            date_id=date_id,
            date=date_str,
            day=date.day,
            month=date.month,
            year=date.year,
            weekday=date.strftime("%A")
        )
        self.dim_dates[date_id] = dim_date
        self._date_string_index[date_str] = date_id
        self._date_counter += 1
        return date_id
    
    def add_signup(self, student_email: str, activity_name: str, 
                   signup_date: Optional[datetime] = None) -> int:
        """Add a fact record for an activity signup"""
        if signup_date is None:
            signup_date = datetime.now()
        
        # Get or create dimension keys
        student_id = self._student_email_index.get(student_email)
        activity_id = self._activity_name_index.get(activity_name)
        
        if student_id is None:
            raise ValueError(f"Student {student_email} not found in dimension table")
        if activity_id is None:
            raise ValueError(f"Activity {activity_name} not found in dimension table")
        
        date_id = self.add_date(signup_date)
        
        # Create fact record
        fact_id = self._fact_counter
        fact = FactActivitySignup(
            fact_signup_id=fact_id,
            student_id=student_id,
            activity_id=activity_id,
            date_id=date_id,
            signup_timestamp=signup_date.isoformat()
        )
        self.fact_signups[fact_id] = fact
        self._fact_counter += 1
        return fact_id
    
    def get_student_by_email(self, email: str) -> Optional[DimStudent]:
        """Get student by email"""
        student_id = self._student_email_index.get(email)
        return self.dim_students.get(student_id) if student_id else None
    
    def get_activity_by_name(self, name: str) -> Optional[DimActivity]:
        """Get activity by name"""
        activity_id = self._activity_name_index.get(name)
        return self.dim_activities.get(activity_id) if activity_id else None
    
    def get_signups_by_student(self, student_email: str) -> List[FactActivitySignup]:
        """Get all signups for a student"""
        student_id = self._student_email_index.get(student_email)
        if not student_id:
            return []
        return [fact for fact in self.fact_signups.values() 
                if fact.student_id == student_id]
    
    def get_signups_by_activity(self, activity_name: str) -> List[FactActivitySignup]:
        """Get all signups for an activity"""
        activity_id = self._activity_name_index.get(activity_name)
        if not activity_id:
            return []
        return [fact for fact in self.fact_signups.values() 
                if fact.activity_id == activity_id]
    
    def get_activity_analytics(self) -> List[Dict]:
        """Get analytics: activity signups count"""
        analytics = []
        for activity_id, activity in self.dim_activities.items():
            signups = [f for f in self.fact_signups.values() 
                      if f.activity_id == activity_id]
            analytics.append({
                "activity_name": activity.activity_name,
                "description": activity.description,
                "schedule": activity.schedule,
                "max_participants": activity.max_participants,
                "current_signups": len(signups),
                "spots_left": activity.max_participants - len(signups)
            })
        return analytics
    
    def get_student_analytics(self) -> List[Dict]:
        """Get analytics: student activity participation"""
        analytics = []
        for student_id, student in self.dim_students.items():
            signups = [f for f in self.fact_signups.values() 
                      if f.student_id == student_id]
            activities = []
            for signup in signups:
                activity = self.dim_activities.get(signup.activity_id)
                if activity:
                    activities.append(activity.activity_name)
            
            analytics.append({
                "student_name": student.name,
                "email": student.email,
                "grade_level": student.grade_level,
                "activities_count": len(activities),
                "activities": activities
            })
        return analytics


# Global star schema instance
star_schema = StarSchemaModel()
