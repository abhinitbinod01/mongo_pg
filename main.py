
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def write():
    return {"message":"My name is Abhinit"}

@app.get("/hello")
def test1():
    return "Hello How are you?"

@app.get("/advi")
def love_advi():

    return "I love you advika"

@app.get("/roshni")
def love_advi():
    return "I love you roshni"

students = {1: "akash",2:"vikash",3:"prakash"}

@app.get("/students")
def get_students():
    return students

@app.get("/students/{student_id}")
def student_search(student_id:int):
    return {"name": students[student_id]}

@app.get("/add_student")
def add_student(student_id:int,student_name:str):
    students[student_id] = student_name
    return students

from pydantic import BaseModel

class Student(BaseModel):
    student_id:int
    student_name:str

@app.post("/add_student_diff")
def add_student(student:Student):
    students[student.student_id] = student.student_name
    return students