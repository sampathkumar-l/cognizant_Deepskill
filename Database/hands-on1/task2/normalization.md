# College Database Normalization Report

## 1NF Verification

### Valid 1NF Example

```sql
INSERT INTO students(first_name, last_name, email, phone, department_id)
VALUES
('Ram', 'Praba', 'rampraba@gmail.com', '9876543210', 1);
```

### Verification

```sql
SELECT * FROM students;
```

| student_id | first_name | last_name  |       email         |    phone    |
| ---------- | ---------- | ---------- | ------------------- | ------------|
| 1          | Ram        |  Praba     | rampraba@gmail.com  |  9876543210 |

The table satisfies 1NF because:

* each attribute contains atomic values
* no repeating groups exist

![alt text](image.png)

---

## Example of 1NF Violation

```sql
INSERT INTO students(first_name, last_name, email, phone, department_id)
VALUES
('Test', 'User', 'test@gmail.com',
'9876543210,34671981821', 1);
```

![alt text](image-1.png)

### Why This Violates 1NF

The phone column stores multiple phone numbers in a single field.

Example:

```text
phone = 9876543210,34671981821
```
This violates 1NF because attributes must contain atomic values only.
And also we have create a column with a specific VARCHAR limit which become exceeded.

---

## Correct Solution

Create a separate table for phone numbers refering to the student_id.

```sql
CREATE TABLE student_phones (
    phone_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(student_id),
    phone_number VARCHAR(15)
);
```

Insert values:

```sql
INSERT INTO student_phones(student_id, phone_number)
VALUES
(1, '9876543210'),
(1, '34671981821');
```

### Verification

| phone_id | student_id | phone_number |
| -------- | ---------- | ------------ |
| 1        | 1          | 9876543210   |
| 2        | 1          | 34671981821  |

Now the design satisfies 1NF.

---

# Conclusion

The original schema satisfies 1NF when atomic values are stored.
Storing multiple phone numbers inside one column violates 1NF.
The normalized solution is to store phone numbers in a separate table.

# 2NF Verification

## Valid 2NF Example

### Verification

```sql id="2g0m4i"
SELECT * FROM enrollments;
```

| student_id | course_id |
| ---------- | --------- |
| 1          | 1         |

The table satisfies 2NF because:

* every non-key attribute depends on the complete primary key
* no partial dependency exists

Composite Key:

```text id="gn10za"
(student_id, course_id)
```

Dependency:

```text id="r6smg8"
(student_id, course_id) → enrollment_date
```

The `enrollment_date` depends on both:

* `student_id`
* `course_id`

Therefore the table satisfies 2NF.

![alt text](image-2.png)
![alt text](image-3.png)
---

## Example of 2NF Violation

Consider the following table structure:

| student_id | course_id | student_name | course_name |
| ---------- | --------- | ------------ | ----------- |
| 1          | 101       | Ram          | DBMS        |



### Why This Violates 2NF

Composite Primary Key:

```text id="x8n8ng"
(student_id, course_id)
```

Dependencies:

```text id="u9bdaz"
student_id → student_name
course_id → course_name
```

Problem:

* `student_name` depends only on `student_id`
* `course_name` depends only on `course_id`

These attributes do not depend on the full primary key.

This creates partial dependency and violates 2NF.

---

## Correct Solution

Separate the tables into:

* students
* courses
* enrollments

This removes partial dependency and redundancy.

---

# Conclusion

The schema satisfies 2NF because:

* all non-key attributes depend on the complete primary key
* no partial dependency exists
* redundancy is reduced

# 3NF Verification

## Valid 3NF Example

### Verification

```sql id="7l7m4d"
SELECT * FROM students;
```

| student_id | student_name | department_id |
| ---------- | ------------ | ------------- |
| 1          | Ram          | 1             |

The table satisfies 3NF because:

* no non-key attribute depends on another non-key attribute
* no transitive dependency exists

![alt text](image-4.png)

---

## Example of 3NF Violation

Consider the following table structure:

| student_id | student_name | department_id | department_name |
| ---------- | ------------ | ------------- | --------------- |
| 1          | Ram          | 10            | ECE             |

![alt text](image-5.png)

### Why This Violates 3NF

Dependencies:

```text id="95mzyv"
student_id → department_id
department_id → department_name
```

Therefore:

```text id="zl9vsl"
student_id → department_name
```

Problem:

* `department_name` depends on `department_id`
* not directly on `student_id`

This creates transitive dependency and violates 3NF.

---

## Correct Solution

Store:

* `department_id` inside students table
* `department_name` only inside departments table

This removes transitive dependency.

---

# Conclusion

The schema satisfies 3NF because:

* no transitive dependency exists
* non-key attributes depend only on the primary key
* redundancy is reduced
