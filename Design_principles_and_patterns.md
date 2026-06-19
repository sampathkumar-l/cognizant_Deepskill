# Design Principles and Patterns:

## Design Principles:

**1.SOLID Principle:**

this the five guidelines that enhance software design maing code more maintainable and sacable. 

- Single Responsibility Principle:

This principle state the one class should be responsible for only one job or single purpose, or we can also say the a class should do only one job within the system.

Example: Instead of creating one huge class called User for login,database,email handling we have create a seperate class for handling all these things seperately.

- Open/Closed Principle:

This principle states that software entities should be open for extension but closed for modification. We should be able to add new functionality without changing existing code.

Example: Instead of modifying the same payment class again and again for Credit Card, UPI, and PayPal, we can create separate classes implementing a common Payment interface.

- Liskov Substitution Principle:

This principle states that child classes should be able to replace parent classes without affecting the correctness of the program.

Example: If Bird class has a fly() method, then Penguin should not inherit from it because penguins cannot fly.

- Interface Segregation Principle:

This principle states that a class should not be forced to implement methods that it does not use.

Example: Instead of creating one large Worker interface with work() and eat(), we can create separate interfaces because a Robot does not need eat() functionality.

- Dependency Inversion Principle:

This principle states that high-level modules should not depend on low-level modules directly. Both should depend on abstractions.

Example: Instead of connecting an application directly with MySQL class, we can use a Database interface so that databases can be changed easily later.

**2.DRY(Don't Repeat Yourself)**

This principle states that duplicate code should be avoided because repeating the same logic in multiple places makes maintenance difficult.

Example: Instead of writing separate tax calculation methods for different vehicles, we can create one common reusable method.

**3.KISS (Keep It Simple Stupid):**

This principle states that software design should be kept as simple as possible and unnecessary complexity should be avoided.

Example: Using simple readable conditions is better than writing overly complex nested logic.

**4.YAGNI (You Aren't Gonna Need It):**

This principle states that developers should not add features unless they are actually needed.

Example: Building extra APIs for future assumptions without any requirement leads to unnecessary complexity.

# Design Patterns

Design patterns are reusable solutions for common problems that occur during software development.
They are not actual code, but they provide a proper structure and approach for solving problems in software design.


# 1. Creational Design Patterns

These patterns mainly focus on object creation or problem related to object creation.
They help in creating objects in a more flexible and efficient way instead of creating objects directly.



* **Singleton Pattern**
  It ensures a class only has one instance, and provides a global point of access to it

  Example: Database connection manager ensure only one shared instance is used across the application.

---

* **Factory Pattern**
  Defines an interface for creating objects but lets subclasses decide which specific object to instantiate.

  Example: Creating different notification objects like Email or SMS using a common interface.

---

* **Builder Pattern**
  Separates the construction of a complex object from its representation, allowing you to create objects step by step. 

  Example: Building a computer with RAM, CPU, and storage configurations.

---

* **Prototype Pattern**
  Creates objects by copying existing objects.

  Example: Cloning an existing employee object.

---

# 2. Structural Design Patterns

These patterns deal with how classes and objects are connected to form larger structures.


### Some Structural Patterns I Learned

* **Adapter Pattern**
  It converts one interface into another that a client expects.

  Example: Mobile charger adapter.

---

* **Decorator Pattern**
  Adds extra functionality to objects dynamically without modifying the code.

  Example: Adding extra toppings to pizza.

---

* **Facade Pattern**
  Provides a simple interface to a complex system,hiding its inner complexity and making it easier to use.

  Example: One button to start an entire computer system.

---

* **Proxy Pattern**
  Acts as a placeholder or surrogate for another object to control access, delay creation, or add extra functionality.

  Example: ATM acting as a middle layer between user and bank server.

---

# 3. Behavioral Design Patterns

These focus on how objects interact and communicate with each other. They help organize responsibilities, encapsulate behavior, and make the system easier to maintain and extend.


### Some Behavioral Patterns I Learned

* **Observer Pattern**
  This pattern defines a one-to-many relationship between objects.
  When one object changes its state, all dependent objects are notified automatically.

  Example:
  YouTube subscribers receiving notifications whenever a creator uploads a new video.

---

* **Strategy Pattern**
  This pattern allows selecting different algorithms or behaviors at runtime.

  Example:
  Different payment methods like UPI, Credit Card, and Net Banking in an e-commerce application.

---

* **Command Pattern**
  This pattern converts a request into an object so that requests can be stored, queued, or undone later.

  Example:
  Undo and redo operations in text editors.

---

* **State Pattern**
  This pattern changes the behavior of an object based on its internal state.

  Example:
  Traffic light system changing behavior between Red, Yellow, and Green states.

---

* **Chain of Responsibility PatternState Pattern**

   This pattern passes requests through multiple handlers until one handler processes the request.

   Example:
   Customer support ticket escalation system.

