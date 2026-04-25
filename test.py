import json
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("DB_URL")

# Assuming Student Pydantic model
class Student(BaseModel):
    id: int
    name: str
    age: int

def get_connection():
    try:
        conn =  psycopg2.connect(DB_URL,cursor_factory=RealDictCursor)
    except Exception as e:
        print(e)
    cursor = conn.cursor()
    return conn,cursor    

app = FastAPI()

def save_file(data):
    print(data)
    # Using 'a' mode to append to file
    with open('sample.txt', 'a') as f:
        # Write formatted string or use json.dump
        f.write(f"{data['id']},{data['name']},{data['age']}\n")

@app.post('/students/create')
def create_student(stud: Student):
    # Use model_dump() (Pydantic v2) or dict() (Pydantic v1)
    # save_file(stud.dict())
    if save_student_db(stud):
        return {"message": "Student record inserted successfully"}

def save_student_db(stud:Student):
    conn,cursor = get_connection()
    query = f"INSERT INTO students(id,name,age) VALUES (%s,%s,%s)"
    cursor.execute(query,(stud.id,stud.name,stud.age))
    conn.commit()
    close_connection(conn,cursor)
    return True


#Write a Python function that takes a student ID as input and retrieves the corresponding student record from the Neon DB database. Expose this function as a GET API endpoint using FastAPI. Ensure proper error handling and return appropriate HTTP status codes (e.g., 404 if the student is not found).
@app.get("/students")
def get_all_student():
    conn,cursor = get_connection()
    query = 'Select * from students'
    cursor.execute(query)
    rows = cursor.fetchall()
    close_connection(conn,cursor)
    return rows

def close_connection(conn,cursor):
    cursor.close()
    conn.close()

#Design a Pydantic model for representing course information, including attributes like 
# course ID (integer), course name (string), credits (integer), and instructor (string). 
# Create a FastAPI POST endpoint that accepts a list of course objects conforming to this model and stores them in a JSON file. Implement appropriate validation to ensure data integrity.
class Course(BaseModel):
    course_id:int
    course_name:str
    credits:int
    instructor:str


@app.post("/courses/add")
def insert_course(courses: list[Course]):
    courseList = [c.model_dump() for c in courses]
    with open('test.json', 'w') as f:
        json.dump(courseList,f,indent=4)
    return "success"

@app.delete("/students/delete")
def delete_student(stud_id:str):
    conn,cursor = get_connection()
    query = "DELETE from students where id=%s"
    cursor.execute(query,(stud_id,))
    conn.commit()
    close_connection(conn,cursor)
    return {"message": "Student deleted successfully"}

@app.put("/students/update")
def update_student(stud_id:str,student:Student):
    conn,cursor = get_connection()
    query = "Select * from students where id=%s"
    cursor.execute(query,(stud_id,))
    student_data = cursor.fetchone()
    if not student_data:
        return {"error": "Student not found"}
        
    query = "Update Students set name= %s, age=%s where id=%s"
    cursor.execute(query,(student.name,student.age,stud_id))
    conn.commit()
    close_connection(conn,cursor)
    return {message: "student record updated successfully"}


 




    

