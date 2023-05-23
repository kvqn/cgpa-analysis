import os
import re
import tomlkit
import json
from typing import TypedDict
import pydantic


class ResultConfig(pydantic.BaseModel):
    output_file: str
    subjects: dict[str, str] # subject name -> subject regex
    input_files: list[str]

class Student(TypedDict):
    sno: int
    name: str
    rollno: str
    grades: dict[str, str]
    tc: int
    cgpa: float
    failed_papers: str

class Result(TypedDict):
    n_students: int
    n_subject_columns_required: int
    students: list[Student]

class FinalStudent(TypedDict):
    name: str
    rollno: str
    grades: list[str]
    tc: int
    cgpa: float
    failed_papers: list[str]

class FinalResult(TypedDict):
    n_students: int
    subjects: list[str]
    students: list[FinalStudent]


def _create_empty_result(config_file: str):
    """
    Create an empty config file.
    """

    print("Creating an empty config file at", config_file)

    config = ResultConfig(
        output_file="",
        subjects={},
        input_files=[]
    )

    with open(config_file, "w") as f:
        tomlkit.dump(config.dict(), f)



def create_sem_result(args):
    """
    Create a semester result according to the specified config file.
    """

    config_file = args.config
    if not os.path.exists(config_file):
        _create_empty_result(config_file)
        return

    with open(config_file, "r") as f:
        config = ResultConfig.parse_obj(tomlkit.parse(f.read()))

    # Check if input files exist
    for file in config.input_files:
        if not os.path.exists(file):
            print("Input file", file, "does not exist.")
            return

    students : dict[str, Student] = {}      # rollno -> student
    for file in config.input_files:
        with open(file, "r") as f:
            data : Result = json.load(f)
            for student in data["students"]:
                rollno = student["rollno"]
                students[rollno] = student

    # Create a new result
    result = FinalResult(
        n_students=len(students),
        subjects=list(config.subjects.keys()),
        students=[]
    )

    # Add students to the result
    for student in students.values():
        final_student = FinalStudent(
            name=student["name"],
            rollno=student["rollno"],
            grades=[],
            tc=student["tc"],
            cgpa=student["cgpa"],
            failed_papers=student["failed_papers"].replace(',', ' ').split(' ')
        )
        for subject_regex in config.subjects.values():
            for subject, grade in student["grades"].items():
                if re.match(subject_regex, subject):
                    final_student["grades"].append(grade)
                    break
            else:
                final_student["grades"].append("")
        result["students"].append(final_student)

    # Write the result to the output file
    with open(config.output_file, "w") as f:
        json.dump(result, f, indent=4)

