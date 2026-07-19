# Hands-On 1 – QA Concepts, Functional Testing & Defect Lifecycle

## Task 1: Map Testing Types to a Real System

### 1. Unit Testing
**Description:**
Unit testing verifies an individual function or module independently without interacting with external components.

**Test Case:**
Test the `create_course()` function to verify that it creates a course object correctly when valid data is provided.

**Type:**
Functional Testing

---

### 2. Integration Testing

**Description:**
Integration testing verifies that two or more modules work correctly together.

**Test Case:**
Send a POST request to `/api/courses/` and verify that the API successfully stores the course information in the database.

**Type:**
Functional Testing

---

### 3. System Testing

**Description:**
System testing validates the complete application from start to finish.

**Test Case:**
Create a course through the API and retrieve it using the GET endpoint to verify that the entire workflow functions correctly.

**Type:**
Functional Testing

---

### 4. User Acceptance Testing (UAT)

**Description:**
User Acceptance Testing ensures the application satisfies business requirements from the user's perspective.

**Test Case:**
A college administrator creates a new course and verifies that it appears in the course list and can be accessed by students.

**Type:**
Functional Testing

---

## Functional vs Non-Functional Testing

### Functional Testing
Functional testing verifies whether the application performs the expected operations according to the requirements.

Example:
- Creating a new course.
- Updating course details.
- Deleting a course.

### Non-Functional Testing

Non-functional testing measures the quality attributes of the application such as performance, security, and reliability.

Example:
Test whether the Course Management API can handle 1000 simultaneous requests while maintaining acceptable response time.

---

## Black-Box Testing vs White-Box Testing

### Black-Box Testing

Black-box testing is performed without any knowledge of the internal source code. The tester validates the functionality by providing inputs and verifying outputs.

Example:
A QA engineer tests the POST `/api/courses/` endpoint by sending requests and checking the responses.

---

### White-Box Testing

White-box testing is performed with complete knowledge of the application's internal code, logic, and implementation.

Example:
A developer writes unit tests for the `create_course()` function and verifies every execution path.

---

### Who Performs Them?

| Testing Type | Performed By |
|--------------|--------------|
| Black-Box Testing | QA Tester |
| White-Box Testing | Developer |

---

# Formal Test Cases

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|---------------|------------|---------------|------------|-----------------|---------------|-----------|
| TC001 | Create a new course with valid data | API server is running | Send POST request with valid course details | HTTP 201 Created and course stored successfully | | |
| TC002 | Create course with missing required field | API server is running | Send POST request without Course Name | HTTP 400 Bad Request with validation message | | |
| TC003 | Create duplicate course | Course already exists | Send POST request using existing Course Code | Error message indicating duplicate course | | |

---

# Task 2: Defect Lifecycle

## Defect Lifecycle

```
New
 ↓
Assigned
 ↓
Open
 ↓
Fixed
 ↓
Retest
 ↓
Verified
 ↓
Closed
```

### Rejected
The defect is rejected if it is not considered a valid bug.

### Deferred
The defect is postponed to a future release because it is not critical or cannot be fixed immediately.

---

# Severity and Priority Classification

## Bug A

**Issue:**
POST `/api/courses/` returns **500 Internal Server Error** for every request.

**Severity:** Critical

**Priority:** P1

**Justification:**
The API is completely unusable and blocks all users from creating courses.

---

## Bug B

**Issue:**
Course names longer than 150 characters are truncated without warning.

**Severity:** Medium

**Priority:** P3

**Justification:**
The application works but data integrity is affected.

---

## Bug C

**Issue:**
Swagger documentation contains a spelling mistake.

**Severity:** Low

**Priority:** P4

**Justification:**
Only documentation is affected and the application functions correctly.

---

## Bug D

**Issue:**
Login sometimes returns HTTP 401 even with correct credentials.

**Severity:** High

**Priority:** P1

**Justification:**
Intermittent login failures reduce reliability and directly impact users.

---

# Defect Report

| Field | Value |
|--------|-------|
| Defect ID | BUG-001 |
| Title | POST /api/courses returns HTTP 500 |
| Environment | Windows 11, Chrome Latest |
| Build Version | v1.0 |
| Severity | Critical |
| Priority | P1 |
| Steps to Reproduce | 1. Open API 2. Send POST request with valid data 3. Observe response |
| Expected Result | Course should be created successfully with HTTP 201 |
| Actual Result | HTTP 500 Internal Server Error is returned |
| Attachments | Screenshot of HTTP 500 Error |

---

# Severity vs Priority

## Severity

Severity indicates the impact of a defect on the application.

Example:
If users cannot log in, the severity is High because a major functionality is broken.

---

## Priority

Priority indicates how quickly the defect should be fixed.

Example:
A spelling mistake on the CEO's dashboard has Low Severity because the application still works, but High Priority because it is highly visible and should be corrected before release.

---

# Conclusion

This hands-on introduced the fundamentals of Quality Assurance, including testing types, functional and non-functional testing, black-box and white-box testing, formal test case design, defect lifecycle, severity and priority classification, and professional defect reporting. These concepts form the foundation of software testing and are essential before learning Selenium automation.