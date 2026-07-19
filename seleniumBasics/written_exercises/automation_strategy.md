# Hands-On 3 – Test Automation Process, Lifecycle & Framework Types

---

# Task 1: Automation Decision and Test Case Selection

## 1. Criteria for Deciding Whether a Test Case Should Be Automated

### 1. Repetitive Execution
Test cases that are executed repeatedly, such as regression tests, should be automated to save time and effort.

**Application to Scenario:**
The POST `/api/courses/` endpoint is tested after every code update, making it an excellent candidate for automation.

---

### 2. Stable Functionality

Automation is most effective when the feature does not change frequently.

**Application to Scenario:**
The course creation API is a core feature and is expected to remain stable.

---

### 3. High Business Impact

Critical functionalities should be automated because failures can significantly affect users.

**Application to Scenario:**
Creating a course is an essential operation, so automated testing ensures reliability.

---

### 4. Data-Driven Testing

Tests that require multiple sets of input data are ideal for automation.

**Application to Scenario:**
The POST endpoint can be tested using various combinations of valid and invalid course details.

---

### 5. Time Saving

Automation reduces manual effort for tests that are run frequently.

**Application to Scenario:**
Instead of manually verifying course creation after every build, automation performs the task quickly and consistently.

---

# Test Case Selection

| Test Case | Decision | Justification |
|-----------|----------|---------------|
| Regression testing for all CRUD endpoints | Automate | Executed after every code change. |
| Exploratory testing of a new search feature | Manual | Requires human judgment and creativity. |
| Performance test with 100 concurrent users | Automate | Performance tools can simulate concurrent users efficiently. |
| UI Login Test | Automate | Login is a stable and frequently tested feature. |
| Verify Swagger Documentation | Manual | Documentation changes infrequently and requires manual review. |
| Smoke Test after Deployment | Automate | Quickly verifies that the application is operational after deployment. |

---

# Test Automation ROI

## Definition

Test Automation Return on Investment (ROI) measures whether the time invested in creating automated tests is recovered through repeated executions.

---

## Given

Time to automate one regression test = **4 hours**

Manual execution time = **30 minutes = 0.5 hours**

Maintenance overhead after the 10th run = **20% of 0.5 hour = 0.1 hour**

---

## ROI Calculation

Automation Cost = 4 hours

Manual Cost per Run = 0.5 hours

Break-even Point:

4 ÷ 0.5 = **8 Runs**

Therefore, after approximately **8 executions**, automation becomes more cost-effective than manual testing.

After the 10th execution, maintenance requires an additional 0.1 hour per run, but automation still provides significant long-term savings.

---

# Flaky Test

## Definition

A flaky test is a test that sometimes passes and sometimes fails without any changes in the application code.

---

## Example

A Selenium test attempts to click a button before the page has completely loaded.

Sometimes the page loads quickly and the test passes.

Sometimes the page loads slowly and the test fails.

---

## Preventing Flaky Tests

1. Replace `time.sleep()` with Explicit Waits.

2. Use reliable locators such as ID or CSS selectors.

3. Execute tests in isolated environments with proper setup and teardown.

---

# Task 2: Automation Framework Types

## 1. Linear Framework

### Description

A Linear Framework executes test cases sequentially from beginning to end. Test scripts contain both test logic and test data in the same file.

### Advantage

Simple to develop.

### Disadvantage

Difficult to maintain for large projects.

### Example

Testing only the Course Login page.

---

## 2. Modular Framework

### Description

The application is divided into independent modules, and separate scripts are written for each module.

### Advantage

Reusable code.

### Disadvantage

Requires more planning during development.

### Example

Separate modules for Login, Courses, Students, and Faculty.

---

## 3. Data-Driven Framework

### Description

Test data is stored separately in files such as Excel, CSV, or JSON while the same test script executes multiple datasets.

### Advantage

Easy to test many input combinations.

### Disadvantage

Additional effort is required to manage test data.

### Example

Testing login with 50 different username and password combinations.

---

## 4. Keyword-Driven Framework

### Description

Testing actions are represented by keywords such as Login, Click, EnterText, and Submit.

### Advantage

Non-technical users can create tests.

### Disadvantage

Complex framework implementation.

### Example

Business analysts preparing test cases using predefined keywords.

---

## 5. Hybrid Framework

### Description

Hybrid Framework combines Modular, Data-Driven, and Keyword-Driven approaches to create a flexible and maintainable automation solution.

### Advantage

Highly reusable and scalable.

### Disadvantage

Initial setup requires more effort.

### Example

Large enterprise applications with multiple modules and extensive regression testing.

---

# Framework Recommendation

For the Course Management System, the recommended approach is a **Hybrid Framework**.

### Justification

- Supports reusable modules.
- Allows testing with multiple datasets.
- Simplifies maintenance.
- Suitable for large Selenium projects.
- Supports both technical and non-technical team members.

---

# Hybrid Framework Folder Structure

```
CourseManagementAutomation/
│
├── tests/
│   ├── test_login.py
│   ├── test_courses.py
│   └── test_students.py
│
├── pages/
│   ├── login_page.py
│   ├── course_page.py
│   └── student_page.py
│
├── test_data/
│   ├── login_data.xlsx
│   └── courses.json
│
├── utilities/
│   ├── driver_factory.py
│   ├── logger.py
│   └── config_reader.py
│
├── config/
│   └── config.ini
│
├── reports/
│
├── screenshots/
│
├── requirements.txt
│
└── README.md
```

---

# Conclusion

Test automation improves software quality by reducing manual effort, increasing execution speed, and improving test coverage. Selecting appropriate test cases for automation and choosing the right framework are essential for building scalable and maintainable Selenium test suites. Among the available framework types, the Hybrid Framework provides the best balance of flexibility, reusability, and maintainability for enterprise applications.