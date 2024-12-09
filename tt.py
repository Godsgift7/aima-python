from csp import CSP, backtracking_search, forward_checking, mac
import pandas as pd

# Load the CSV file
data = pd.read_csv("../h3-data.csv")

# Extract necessary details
courses = data['Μάθημα'].tolist()
semesters = data['Εξάμηνο'].tolist()
professors = data['Καθηγητής'].tolist()
difficulty = data['Δύσκολο (TRUE/FALSE)'].tolist()
labs = data['Εργαστήριο (TRUE/FALSE)'].tolist()

# Define timeslots
DAYS = 21
PERIODS_PER_DAY = 3
timeslots = [(day, period) for day in range(1, DAYS + 1) for period in range(1, PERIODS_PER_DAY + 1)]

# Define variables, domains, and constraints
variables = courses
domains = {course: timeslots for course in variables}

neighbors = {course: [other for other in variables if other != course] for course in variables}


# Define constraints
def no_overlap(course1, time1, course2, time2):
    return time1 != time2

def different_days_for_same_semester(course1, time1, course2, time2):
    if semesters[courses.index(course1)] == semesters[courses.index(course2)]:
        return time1[0] != time2[0]
    return True

def difficult_courses_spacing(course1, time1, course2, time2):
    if difficulty[courses.index(course1)] and difficulty[courses.index(course2)]:
        return abs(time1[0] - time2[0]) >= 2
    return True

def same_professor_different_days(course1, time1, course2, time2):
    if professors[courses.index(course1)] == professors[courses.index(course2)]:
        return time1[0] != time2[0]
    return True

def lab_follows_theory(course1, time1, course2, time2):
    if labs[courses.index(course1)] and course2 == course1:
        return time1[0] == time2[0] and time2[1] == time1[1] + 1
    return True

class ExamTimetablingCSP(CSP):
    def __init__(self, variables, domains, neighbors):
        # Call the parent constructor with the constraints function passed as an argument
        super().__init__(variables, domains, neighbors, self.constraints)

    def constraints(self, A, a, B, b):
        """Define the constraint logic here."""
        return (
            no_overlap(A, a, B, b)
            and different_days_for_same_semester(A, a, B, b)
            and difficult_courses_spacing(A, a, B, b)
            and same_professor_different_days(A, a, B, b)
            and lab_follows_theory(A, a, B, b)
        )


exam_csp = ExamTimetablingCSP(variables, domains, neighbors)

# Solve CSP using Forward Checking
solution = backtracking_search(exam_csp, inference=forward_checking)

# Output the solution
print("Exam Timetable:", solution)

# Print the timetable in a readable format
print(f"{'Course':<50} {'Day':<5} {'Period':<6}")
print("-" * 65)

for course, (day, period) in solution.items():
    print(f"{course:<50} {day:<5} {period:<6}")
