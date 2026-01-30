# Application Architecture

## Overview

This project follows a **loader-based, layered architecture** designed to make application startup predictable, testable, and scalable. Instead of initializing everything inside a single entry file, responsibilities are broken down into isolated loaders that are executed in a strict order.

---

## High-Level Startup Flow

```
server.js
   ↓
Configuration Loader
   ↓
Logger Initialization
   ↓
Data Source (Proxy / Fake DB)
   ↓
Express App Loader
   ↓
Middlewares
   ↓
Routes
   ↓
HTTP Server Listening
```

Each step depends only on what came before it. If any step fails, the application exits immediately, preventing partial or inconsistent startup.

---

## Entry Point: `server.js`

### Responsibility

* Acts as the **orchestrator** of the application
* Does not contain business logic
* Controls startup order
* Handles fatal startup failures

### Why this matters

Keeping `server.js` thin ensures that:

* Startup logic is easy to reason about
* Individual components can be tested in isolation
* The application can later be adapted for workers, clustering, or serverless environments

---

## Configuration Management

### Location

`src/config/index.js`

### Purpose

* Load environment-specific configuration
* Isolate configuration from application logic
* Fail fast when required variables are missing

### Environment Isolation Strategy

Multiple environment files are supported:

* `.env.local`
* `.env.dev`
* `.env.prod`

The active file is selected using `NODE_ENV`. This prevents accidental leakage of production settings into local or development environments.

### Validation

Required variables (such as `PORT` and `DATA_SOURCE`) are validated at startup. If a variable is missing, the application crashes immediately instead of failing silently at runtime.

---

## Logging Architecture

### Location

`src/utils/logger.js`

### Logging Tool

Winston is used to provide:

* Structured logs
* Consistent formatting
* Centralized logging configuration

### Design Decisions

* `console.log` is avoided entirely
* All startup steps log their completion
* Errors during startup are logged before process termination

### Benefits

* Clear visibility into application state
* Easier debugging in development
* Production-ready logging without refactoring

---

## Data Source Loader (Proxy / Fake DB)

### Location

`src/loaders/db.js`

### Purpose

* Simulate an external dependency
* Preserve async initialization contract
* Allow seamless replacement with a real database later

### Why a Fake DB is Used

At this stage, the focus is architectural rather than data persistence. Using a proxy data source allows:

* Validation of startup sequencing
* Realistic async behavior
* Zero coupling to a specific database technology

This loader can later be replaced with a real database connection without changing the rest of the system.

---

## Express App Loader

### Location

`src/loaders/app.js`

### Responsibility

* Create the Express application instance
* Register global middlewares
* Mount routes
* Log application readiness

### Middleware Strategy

Middlewares are loaded before routes to ensure:

* Consistent request parsing
* Predictable request life-cycle
* Centralized behavior (e.g., JSON handling)

### Route Registration

Routes are mounted explicitly, and route counts are tracked manually at registration time. This avoids reliance on Express private APIs and ensures stability across versions.

---

## Loader Pattern Explained

### What is a Loader?

A loader is a module responsible for initializing **one and only one concern**.

Examples:

* Config loader → configuration
* DB loader → data source
* App loader → Express initialization

### Why Loaders Matter

* Prevents tangled initialization logic
* Enables ordered startup
* Improves test-ability
* Encourages clear ownership of responsibilities

---

## Folder Structure Philosophy

```
src/
 ├── config/        # Environment and configuration logic
 ├── loaders/       # Application initialization units
 ├── utils/         # Cross-cutting utilities (logger, helpers)
 └── server.js      # Application entry point
```

### Design Principles

* No circular dependencies
* Utilities are stateless
* Loaders perform side effects
* Entry point coordinates, not executes

This structure scales naturally as the application grows.

---

## Error Handling Strategy

* Startup errors are treated as fatal
* The process exits immediately on failure
* Errors are logged before termination

This prevents partially initialized systems, which are often harder to debug than immediate failures.

---

## Observability During Startup

The application logs every major initialization milestone:

* Environment selection
* Data source connection
* Middleware loading
* Route mounting
* Server readiness

This creates a clear and auditable startup timeline.

---

## Scalability and Future Extensions

This architecture is designed to support:

* Node.js clustering
* Worker processes
* Graceful shutdown handling
* Real database integration
* Feature-based route modules

No structural refactor is required to support these changes.

---

## Practical Exposure & Engineering Rationale

This architecture has been designed and implemented incrementally through hands-on development rather than theoretical abstraction. Each component reflects real-world back-end practices commonly observed in production-grade Node.js services.

* The **loader-based startup sequence** mirrors patterns used in scalable systems, ensuring deterministic initialization and easier debugging during failures.
* Environment-specific configuration handling replicates how applications are deployed across local, development, and production environments without code changes.
* Centralized logging simulates operational visibility expected in real deployments, enabling engineers to trace startup behavior and diagnose issues early.
* Route introspection and startup metrics provide immediate feedback on application health, a practice frequently adopted in professional back-end teams.

This structure prioritizes maintainability, clarity, and future extensibility, making it suitable for continued development, on boarding new contributors, and real-world back-end workflows.
