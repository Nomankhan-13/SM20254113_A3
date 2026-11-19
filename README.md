# Student Gradebook Manager - ICT102 Assessment 3

**Student Name:** Noman Khan  
**Student ID:** SM20254113  
**Project:** B - Student Gradebook  

## How to run

1. Make sure you have Python 3 installed.
2. Open terminal / command prompt in this folder.
3. Run the program:

```
python gradebook.py
```

or

```
python3 gradebook.py
```

## Features

- Add, View, Search, Update, Delete student records
- Calculate final mark (average of 3 assessments) and assign grade (HD/DN/CR/PS/FL)
- Rank students by final mark
- Summary report (class average, highest/lowest, grade counts)
- Data is saved automatically to `data/students.csv` when you exit
- Input validation so program does not crash on bad input
- One recursive function used for calculating total marks

## Sample data

The `data/students.csv` file already contains 10 sample student records so you can test the program immediately.
##npotes
- Grades follow standard boundaries:  
  HD 85+, DN 75-84, CR 65-74, PS 50-64, FL below 50
- Final mark is calculated as simple average of the three assessment marks.


