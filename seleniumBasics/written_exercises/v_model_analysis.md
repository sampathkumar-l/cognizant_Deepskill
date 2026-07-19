# Hands-On 2 – SDLC vs TDLC, V-Model & Agile QA Integration

---

# Task 1: V-Model Mapping

## V-Model Diagram

```
                SDLC (Development)

        Requirements
             │
             ▼
        System Design
             │
             ▼
      Architecture Design
             │
             ▼
         Module Design
             │
             ▼
             Coding
             ▲
             │
         Unit Testing
             ▲
             │
     Integration Testing
             ▲
             │
        System Testing
             ▲
             │
     Acceptance Testing

              TDLC (Testing)
```

---

## SDLC to TDLC Mapping

| SDLC Phase | Corresponding TDLC Phase | Test Artifact Produced |
|------------|--------------------------|------------------------|
| Requirements Analysis | Acceptance Testing | Acceptance Test Plan |
| System Design | System Testing | System Test Cases |
| Architecture Design | Integration Testing | Integration Test Cases |
| Module Design | Unit Testing | Unit Test Cases |
| Coding | Execution of Test Cases | Executable Software |

---

## Entry and Exit Criteria

### 1. Unit Testing

**Entry Criteria**
- Module development completed.
- Source code available.
- Unit test cases prepared.

**Exit Criteria**
- All unit test cases executed.
- No critical defects remain.
- Code coverage meets project standards.

---

### 2. Integration Testing

**Entry Criteria**
- All modules successfully pass unit testing.
- Integration environment is ready.

**Exit Criteria**
- Module interactions are verified.
- Major integration defects are fixed.

---

### 3. System Testing

**Entry Criteria**
- Complete application is deployed.
- Functional requirements are finalized.

**Exit Criteria**
- All planned system test cases executed.
- Critical and High severity defects closed.
- Application satisfies business requirements.

---

### 4. Acceptance Testing

**Entry Criteria**
- System testing completed successfully.
- Customer-approved build available.

**Exit Criteria**
- Customer accepts the application.
- Acceptance criteria satisfied.
- Product approved for deployment.

---

## QA Engagement Points

QA should actively participate during the following SDLC phases:

### Requirements Analysis

- Review requirements for completeness.
- Identify ambiguous or missing requirements.
- Prepare high-level test scenarios.

### System Design

- Review system architecture.
- Identify potential testing challenges.
- Design test strategy and test plan.

Early QA involvement reduces defects and lowers the cost of fixing issues later in development.

---

# Task 2: Agile QA and Shift-Left Testing

## Problems with Waterfall Testing

### Problem 1

Defects are discovered very late, making them expensive and time-consuming to fix.

---

### Problem 2

Developers may misunderstand requirements, resulting in major rework during testing.

---

### Problem 3

Testing time becomes limited near the release date, reducing overall software quality.

---

## QA Responsibilities in Agile

### Sprint Planning

- Review user stories.
- Define acceptance criteria.
- Estimate testing effort.

---

### Daily Stand-up

- Share testing progress.
- Report blockers.
- Coordinate with developers regarding defects.

---

### Sprint Review

- Demonstrate completed features.
- Verify acceptance criteria.
- Confirm business requirements are met.

---

### Sprint Retrospective

- Discuss testing improvements.
- Review defects found during the sprint.
- Suggest process improvements for future sprints.

---

## Shift-Left Testing Practices

### 1. Requirement Reviews

QA reviews requirements before development begins to identify ambiguities and improve testability.

---

### 2. Test Case Design Before Coding

QA prepares test cases before implementation so developers clearly understand expected behavior.

---

### 3. Static Code Analysis

Developers use static analysis tools to identify coding issues before executing the application.

---

### 4. API Contract Testing

API request and response formats are validated before integrating different modules, reducing integration issues.

---

# Acceptance Criteria (Given-When-Then)

## Scenario 1 – Successful Course Creation

**Given**
The administrator is logged into the Course Management System.

**When**
The administrator enters valid course details and submits the form.

**Then**
The course is created successfully and appears in the course list.

---

## Scenario 2 – Duplicate Course Code

**Given**
A course already exists with course code "CS101".

**When**
The administrator attempts to create another course using "CS101".

**Then**
The system displays an error indicating that the course code already exists.

---

## Scenario 3 – Missing Required Fields

**Given**
The administrator opens the Create Course page.

**When**
The administrator submits the form without entering mandatory fields.

**Then**
Validation messages are displayed and the course is not created.

---

# Conclusion

The V-Model establishes a direct relationship between software development and testing activities, ensuring each development phase has a corresponding testing phase. Agile QA encourages continuous collaboration, while Shift-Left Testing promotes early defect detection through proactive testing practices. Together, these approaches improve software quality, reduce development costs, and enable faster delivery of reliable applications.