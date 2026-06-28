# ============================================================
# Task 1: Understanding the Django Request-Response Cycle
# ============================================================

# ------------------------------------------------------------
# 1. Journey of a GET /api/courses/ Request
# ------------------------------------------------------------

# Example Request:
# Browser ---> GET /api/courses/

# Step 1:
# The user enters the URL (http://127.0.0.1:8000/api/courses/)
# in the browser. The browser sends an HTTP GET request to the
# Django application.

# Step 2:
# Django receives the request. Before it reaches the application,
# the request passes through the middleware.

# Step 3:
# The URL Router (urls.py) checks the requested URL and matches
# it with the appropriate view.

# Example:
# path("api/courses/", views.course_list)

# Step 4:
# The matched View (views.py) is executed. The view contains the
# business logic required to process the request.

# Step 5:
# If data is needed, the View communicates with the Model.

# Example:
# courses = Course.objects.all()

# Step 6:
# The Model interacts with the database and retrieves the
# requested records.

# Step 7:
# The retrieved data is returned to the View.

# Step 8:
# The View prepares an HTTP response.
# This response could be:
# - JSON (for APIs)
# - HTML page
# - Redirect
# - Error response

# Step 9:
# Before sending the response back to the browser, it again
# passes through the middleware.

# Step 10:
# Finally, Django sends the HTTP response back to the browser,
# where the user sees the requested data.

# Overall Request Flow:
#
# Browser
#    |
#    v
# HTTP GET Request
#    |
#    v
# Middleware
#    |
#    v
# URL Router (urls.py)
#    |
#    v
# View (views.py)
#    |
#    v
# Model (models.py)
#    |
#    v
# Database
#    |
#    v
# Model returns data
#    |
#    v
# View creates response
#    |
#    v
# Middleware
#    |
#    v
# HTTP Response
#    |
#    v
# Browser


# ------------------------------------------------------------
# 2. Middleware
# ------------------------------------------------------------

# Middleware is a layer between the incoming request and the
# Django view. It processes requests before they reach the view
# and processes responses before they are returned to the client.

# Request Flow:
# Client --> Middleware --> View

# Response Flow:
# View --> Middleware --> Client

# Two built-in Django middleware classes:

# 1. django.middleware.security.SecurityMiddleware
#
# Purpose:
# - Adds several security features.
# - Helps protect against common web attacks.
# - Supports HTTPS redirects.
# - Sets security-related HTTP headers.

# 2. django.contrib.sessions.middleware.SessionMiddleware
#
# Purpose:
# - Enables session support.
# - Stores and retrieves user session data.
# - Allows users to stay logged in across multiple requests.


# ------------------------------------------------------------
# 3. WSGI vs ASGI
# ------------------------------------------------------------

# WSGI (Web Server Gateway Interface)
#
# - Standard interface between a web server and a Python web
#   application.
# - Designed for synchronous applications.
# - Handles one request per worker at a time.
# - Suitable for traditional web applications.

# ASGI (Asynchronous Server Gateway Interface)
#
# - Successor to WSGI.
# - Supports asynchronous programming.
# - Can handle multiple requests concurrently.
# - Supports WebSockets, long-lived connections, and real-time
#   applications such as chat systems and live notifications.

# Which one does Django use by default?
#
# Django traditionally uses WSGI for deployment.
# Newer versions of Django also support ASGI, making it possible
# to build asynchronous applications.

# When should ASGI be used?
#
# ASGI should be used when the application requires:
# - Real-time communication
# - WebSockets
# - Live chat applications
# - Streaming services
# - High-concurrency asynchronous processing


# ------------------------------------------------------------
# 4. MVC Pattern and Django's MVT Architecture
# ------------------------------------------------------------

# MVC stands for:
#
# M - Model
#     Handles the application's data and interacts with the database.
#
# V - View
#     Displays information to the user (User Interface).
#
# C - Controller
#     Receives user requests, processes business logic, and
#     communicates between the Model and the View.

# Django follows the MVT (Model-View-Template) architecture.

# M - Model
#     Responsible for database operations and data management.

# V - View
#     Contains the business logic.
#     Receives requests, interacts with the Model, and returns
#     responses.

# T - Template
#     Responsible for presenting data to the user.
#     It generates the HTML shown in the browser.

# MVC to MVT Mapping

# MVC                     Django (MVT)
# ---------------------------------------------
# Model        ---------> Model
# View         ---------> Template
# Controller   ---------> View

# In Django:
# - The Model remains the same.
# - Django's View performs the role of the Controller.
# - Django's Template performs the role of the View in MVC.


# ------------------------------------------------------------
# Conclusion
# ------------------------------------------------------------

# The Django request-response cycle begins when a browser sends
# an HTTP request. The request passes through middleware, is
# routed to the appropriate view, which interacts with the model
# to retrieve data from the database. The view then prepares a
# response, which again passes through middleware before being
# returned to the browser. Django uses the MVT architecture,
# where the View acts like the Controller in MVC, while the
# Template represents the user interface. WSGI is suitable for
# synchronous web applications, whereas ASGI is preferred for
# asynchronous and real-time applications.