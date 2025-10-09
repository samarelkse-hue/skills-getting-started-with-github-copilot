"""
Excel Data Loader for Star Schema

This module handles loading data from Excel files and populating
the star schema model.
"""

import pandas as pd
from typing import List, Dict
from pathlib import Path
from datetime import datetime
from star_schema import StarSchemaModel


class ExcelDataLoader:
    """Load data from Excel files into the star schema"""
    
    def __init__(self, star_schema: StarSchemaModel):
        self.star_schema = star_schema
    
    def load_students_from_excel(self, file_path: str, sheet_name: str = "Students") -> int:
        """
        Load students from Excel file
        
        Expected columns: email, name, grade_level
        """
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            count = 0
            
            for _, row in df.iterrows():
                self.star_schema.add_student(
                    email=str(row['email']),
                    name=str(row['name']),
                    grade_level=int(row['grade_level'])
                )
                count += 1
            
            return count
        except Exception as e:
            raise Exception(f"Error loading students from Excel: {str(e)}")
    
    def load_activities_from_excel(self, file_path: str, sheet_name: str = "Activities") -> int:
        """
        Load activities from Excel file
        
        Expected columns: activity_name, description, schedule, max_participants
        """
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            count = 0
            
            for _, row in df.iterrows():
                self.star_schema.add_activity(
                    activity_name=str(row['activity_name']),
                    description=str(row['description']),
                    schedule=str(row['schedule']),
                    max_participants=int(row['max_participants'])
                )
                count += 1
            
            return count
        except Exception as e:
            raise Exception(f"Error loading activities from Excel: {str(e)}")
    
    def load_signups_from_excel(self, file_path: str, sheet_name: str = "Signups") -> int:
        """
        Load signups from Excel file
        
        Expected columns: student_email, activity_name, signup_date (optional)
        """
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            count = 0
            
            for _, row in df.iterrows():
                signup_date = None
                if 'signup_date' in df.columns and pd.notna(row['signup_date']):
                    signup_date = pd.to_datetime(row['signup_date'])
                
                self.star_schema.add_signup(
                    student_email=str(row['student_email']),
                    activity_name=str(row['activity_name']),
                    signup_date=signup_date
                )
                count += 1
            
            return count
        except Exception as e:
            raise Exception(f"Error loading signups from Excel: {str(e)}")
    
    def load_all_from_excel(self, file_path: str) -> Dict[str, int]:
        """
        Load all data from a multi-sheet Excel file
        
        Expected sheets: Students, Activities, Signups
        """
        results = {}
        
        # Load in order: dimensions first, then facts
        try:
            results['students'] = self.load_students_from_excel(file_path)
        except Exception as e:
            results['students'] = f"Error: {str(e)}"
        
        try:
            results['activities'] = self.load_activities_from_excel(file_path)
        except Exception as e:
            results['activities'] = f"Error: {str(e)}"
        
        try:
            results['signups'] = self.load_signups_from_excel(file_path)
        except Exception as e:
            results['signups'] = f"Error: {str(e)}"
        
        return results
    
    def load_from_csv(self, students_csv: str = None, activities_csv: str = None, 
                     signups_csv: str = None) -> Dict[str, int]:
        """
        Load data from CSV files
        
        Alternative to Excel for simpler data sources
        """
        results = {}
        
        if students_csv:
            try:
                df = pd.read_csv(students_csv)
                count = 0
                for _, row in df.iterrows():
                    self.star_schema.add_student(
                        email=str(row['email']),
                        name=str(row['name']),
                        grade_level=int(row['grade_level'])
                    )
                    count += 1
                results['students'] = count
            except Exception as e:
                results['students'] = f"Error: {str(e)}"
        
        if activities_csv:
            try:
                df = pd.read_csv(activities_csv)
                count = 0
                for _, row in df.iterrows():
                    self.star_schema.add_activity(
                        activity_name=str(row['activity_name']),
                        description=str(row['description']),
                        schedule=str(row['schedule']),
                        max_participants=int(row['max_participants'])
                    )
                    count += 1
                results['activities'] = count
            except Exception as e:
                results['activities'] = f"Error: {str(e)}"
        
        if signups_csv:
            try:
                df = pd.read_csv(signups_csv)
                count = 0
                for _, row in df.iterrows():
                    signup_date = None
                    if 'signup_date' in df.columns and pd.notna(row['signup_date']):
                        signup_date = pd.to_datetime(row['signup_date'])
                    
                    self.star_schema.add_signup(
                        student_email=str(row['student_email']),
                        activity_name=str(row['activity_name']),
                        signup_date=signup_date
                    )
                    count += 1
                results['signups'] = count
            except Exception as e:
                results['signups'] = f"Error: {str(e)}"
        
        return results
