# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a comprehensive Python monorepo for "Full-Stack-Python-Kit" that provides a complete development environment for building CLI applications, GUI desktop apps, and full-stack web applications using modern Python technologies.

## Guidelines

You are to never interact with git directly, always just write the git commit message to the screen for the user to copy and paste and commit themselves.

## Project Structure

```
full-stack-python-kit/
├── apps/
│   ├── cli/                    # Typer-based CLI application
│   │   └── main.py            # CLI entry point with rich features
│   ├── gui/                    # NiceGUI desktop application
│   │   └── main.py            # GUI app with dark theme
│   └── webapp/                 # Full-stack web application
│       ├── backend/           # FastAPI backend
│       │   ├── app/          # Application logic
│       │   ├── migrations/    # Alembic database migrations
│       │   ├── main.py       # FastAPI app entry point
│       │   └── alembic.ini   # Migration configuration
│       └── frontend/          # Next.js frontend
│           ├── src/          # Source code
│           ├── package.json  # Dependencies
│           └── *.config.js   # Configuration files
├── packages/                   # Shared Python packages
│   ├── core/                  # Core utilities and config
│   ├── auth/                  # Authentication utilities
│   └── database/              # Database models and session
├── tests/                      # Test suite
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   └── e2e/                   # End-to-end tests
├── pyproject.toml             # Python project configuration
├── justfile                   # Development commands
└── .gitignore                 # Git ignore rules
```

## Development Commands

The project uses `just` as a command runner. Key commands:

### Setup and Installation
- `just setup` - Setup development environment with uv
- `just install` - Install dependencies
- `just install-dev` - Install development dependencies

### Code Quality
- `just format` - Format code with ruff
- `just lint` - Lint code with ruff
- `just typecheck` - Type check with mypy
- `just check` - Run all quality checks (lint + typecheck)

### Testing
- `just test` - Run pytest test suite
- `just test-cov` - Run tests with coverage report

### Running Applications
- `just run-cli [args]` - Run CLI application
- `just run-gui` - Run GUI desktop application
- `just run-webapp-dev` - Run FastAPI backend in development mode
- `just run-webapp-frontend` - Run Next.js frontend in development mode
- `just dev` - Start all services for development

### Database Management
- `just db-upgrade` - Apply database migrations
- `just db-downgrade` - Rollback last migration
- `just db-revision "message"` - Create new migration

### Background Tasks
- `just celery-worker` - Start Celery worker
- `just celery-beat` - Start Celery beat scheduler
- `just flower` - Start Flower monitoring

### Maintenance
- `just clean` - Clean build artifacts and cache files
- `just update` - Update dependencies
- `just info` - Show project information

## Architecture Notes

### Backend (FastAPI)
- Located in `apps/webapp/backend/`
- Uses SQLModel for database ORM with PostgreSQL
- JWT-based authentication with FastAPI Users patterns
- Async/await throughout for performance
- WebSocket support for real-time features
- Structured logging with structlog
- Comprehensive API documentation at `/api/v1/docs`

### Frontend (Next.js)
- Located in `apps/webapp/frontend/`
- TypeScript + React 18 with App Router
- Material-UI components with dark theme
- Zustand for state management
- React Query for API data fetching
- WebSocket integration for real-time updates
- Tailwind CSS for utility styling

### CLI Application
- Built with Typer for type-safe CLI interfaces
- Rich library for beautiful terminal output
- Includes file operations, API testing, and system info
- Subcommands: file, api, system with various operations

### GUI Application
- Built with NiceGUI for cross-platform desktop apps
- Dark theme with multiple tabs and features
- System monitoring, API testing, and file exploration
- Real-time updates and interactive components

### Shared Packages
- `packages/core/` - Configuration, logging, utilities
- `packages/auth/` - Authentication and JWT handling
- `packages/database/` - SQLModel models and session management

### Testing Strategy
- Unit tests for individual components
- Integration tests for API endpoints
- pytest fixtures for database and authentication
- Test coverage reporting
- Async test support with pytest-asyncio

## Environment Variables

Key environment variables (create `.env` file):
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `SECRET_KEY` - JWT secret key (change in production)
- `DEBUG` - Enable debug mode
- `CORS_ORIGINS` - Allowed CORS origins
- `SENTRY_DSN` - Sentry error tracking (optional)

## Database Setup

1. Install PostgreSQL and Redis locally
2. Create database: `createdb fspk_db`
3. Run migrations: `just db-upgrade`
4. Start Redis: `redis-server`

## Production Deployment

The stack is designed for production deployment with:
- Caddy for automatic HTTPS and reverse proxy
- Docker containerization support
- Environment-based configuration
- Health check endpoints
- Metrics and monitoring integration
- Structured logging for observability

## Tech Stack (Strict Adherence Required)

# **The Full-Stack Python Kit**

---

This stack is designed for building feature-rich, scalable web applications, APIs, and desktop tools with Python. It combines battle-tested libraries with modern Python idioms to enhance developer productivity and type safety. The result is a stack that prioritizes rapid development, performance, and long-term maintainability.

---

### **Frontend: Type-Safe & Component-Driven**

This frontend architecture delivers production-ready web applications by combining React's ecosystem with TypeScript for type safety and modern tooling for optimal performance.

- [**Next.js 14+**](https://nextjs.org/docs)
  - **Role:** Full-Stack React Framework.
  - **Description:** A production-ready React framework featuring server-side rendering, static site generation, and API routes. The App Router provides file-based routing and built-in performance optimizations.
- [**React 18+**](https://react.dev/reference/react)
  - **Role:** Component-Based UI Library.
  - **Description:** The industry-standard library for building user interfaces with reusable components, featuring concurrent capabilities for improved performance and user experience.
- [**TypeScript 5+**](https://www.typescriptlang.org/docs/)
  - **Role:** Static Type System for JavaScript.
  - **Description:** Adds compile-time type checking to JavaScript, catching errors early and enabling superior IDE support with autocomplete and safe refactoring.
- [**Tailwind CSS 3.4+**](https://tailwindcss.com/docs/installation)
  - **Role:** Utility-First CSS Framework.
  - **Description:** Enables rapid UI development by composing utility classes directly in your markup, ensuring consistent and maintainable styling without custom CSS.
- [**Material-UI (MUI) 5+**](https://mui.com/material-ui/getting-started/)
  - **Role:** React Component Library.
  - **Description:** A comprehensive library of pre-built, accessible React components that follow Google's Material Design guidelines to accelerate development.
- [**Zustand 4+**](https://docs.pmnd.rs/zustand/getting-started/introduction)
  - **Role:** Lightweight State Management Library.
  - **Description:** A small, fast, and scalable state management solution that provides a simple API for managing global state in React applications.
- [**Vite 5+**](https://vitejs.dev/guide/)
  - **Role:** Frontend Build Tool.
  - **Description:** An ultra-fast development server and build tool that leverages native ES modules for instant hot module replacement and lightning-fast builds.

---

### **Backend: Fast, Type-Safe & API-First**

This backend foundation prioritizes performance and developer productivity, featuring automatic API documentation, type safety, and modern async Python patterns.

- [**FastAPI 0.109+**](https://fastapi.tiangolo.com/)
  - **Role:** High-Performance Web Framework.
  - **Description:** A modern web framework for building APIs with Python, providing automatic interactive documentation, data validation, and native async support.
- [**SQLModel**](https://sqlmodel.tiangolo.com/)
  - **Role:** SQL Database ORM.
  - **Description:** Seamlessly combines SQLAlchemy's database power with Pydantic's data validation for type-safe database operations and automatic serialization.
- [**Uvicorn**](https://www.uvicorn.org/)
  - **Role:** High-Performance ASGI Server.
  - **Description:** A lightning-fast ASGI server that serves as the production-ready engine for FastAPI and other async Python web applications.
- [**Pydantic V2**](https://docs.pydantic.dev/latest/)
  - **Role:** Data Validation Library.
  - **Description:** Leverages Python type hints to validate, serialize, and deserialize data with significant performance, integrating seamlessly with FastAPI.

---

### **GUI & CLI Applications: Python-Native & Cross-Platform**

This combination enables the creation of modern desktop applications and command-line tools using Python.

- [**NiceGUI**](https://nicegui.io/)
  - **Role:** Web-Based Python GUI Framework.
  - **Description:** A framework for building web-based user interfaces and native desktop applications using pure Python and a rich set of UI components.
- [**Typer**](https://typer.tiangolo.com/)
  - **Role:** Modern CLI Framework.
  - **Description:** Uses Python type hints to generate intuitive and maintainable command-line interfaces with automatic help generation, validation, and shell completion.

---

### **Database & Caching: Scalable & Reliable**

This data layer combines PostgreSQL's robustness with Redis's speed for a foundation that scales from development to production.

- [**PostgreSQL 15+**](https://www.postgresql.org/docs/15/index.html)
  - **Role:** Advanced Open-Source Relational Database.
  - **Description:** A leading open-source relational database known for its reliability, performance, and robust feature set suitable for modern applications.
- [**Redis 7+**](https://redis.io/docs/)
  - **Role:** In-Memory Data Store.
  - **Description:** An in-memory database used as a high-performance cache, message broker, and session store to support real-time application features.
- [**Alembic**](https://alembic.sqlalchemy.org/en/latest/)
  - **Role:** Database Migration Tool.
  - **Description:** The standard migration tool for SQLAlchemy, providing a framework for creating, managing, and applying database schema changes in a version-controlled manner.

---

### **Development Workflow: Modern & Fast**

A cutting-edge Python development environment emphasizing speed, consistency, and developer experience through modern tooling.

- [**uv**](https://docs.astral.sh/uv/)
  - **Role:** Python Package and Project Manager.
  - **Description:** An extremely fast, all-in-one tool written in Rust that replaces pip, venv, and more, providing 10-100x faster package management.
- [**Ruff**](https://docs.astral.sh/ruff/)
  - **Role:** High-Performance Python Linter and Formatter.
  - **Description:** A linter and formatter written in Rust that provides sub-second feedback, combining the functionality of tools like Flake8, Black, and isort.
- [**mypy**](https://mypy.readthedocs.io/en/stable/)
  - **Role:** Static Type Checker.
  - **Description:** The standard static type checker for Python, helping to catch type-related errors before runtime and ensuring code correctness.
- [**just**](https://github.com/casey/just)
  - **Role:** Command Runner.
  - **Description:** A simple tool for saving and running project-specific commands and tasks, serving as a cross-platform alternative to `make`.

---

### **Testing: Comprehensive & Developer-Friendly**

A complete testing ecosystem covering unit, integration, API, and end-to-end testing with excellent async support.

- [**pytest**](https://docs.pytest.org/en/latest/)
  - **Role:** Python Testing Framework.
  - **Description:** A popular testing framework offering a simple syntax, powerful fixtures, and an extensive plugin ecosystem for writing and running tests.
- [**pytest-asyncio**](https://pytest-asyncio.readthedocs.io/en/latest/)
  - **Role:** Async Testing Plugin for pytest.
  - **Description:** Enables seamless testing of `asyncio`based code with pytest, essential for applications built with FastAPI and other async frameworks.
- [**httpx**](https://www.python-httpx.org/)
  - **Role:** Modern HTTP Client.
  - **Description:** A fully featured HTTP client library for Python with both synchronous and asynchronous support, ideal for testing APIs.
- [**Playwright**](https://playwright.dev/python/)
  - **Role:** End-to-End Testing Framework.
  - **Description:** A modern framework for reliable end-to-end testing and automation that works across all major browsers with excellent debugging capabilities.

---

### **Authentication & Security: Production-Ready**

A robust security implementation following industry best practices for authentication, authorization, and data protection.

- [**FastAPI Users**](https://fastapi-users.github.io/fastapi-users/)
  - **Role:** Authentication System for FastAPI.
  - **Description:** A flexible and customizable user management system providing registration, authentication, and password management with multi-backend support.
- [**python-jose[cryptography]**](https://python-jose.readthedocs.io/en/latest/)
  - **Role:** JSON Web Token (JWT) Library.
  - **Description:** A JOSE implementation for handling JWT, JWS, and JWK, essential for implementing secure, stateless authentication in web applications.
- [**passlib[bcrypt]**](https://passlib.readthedocs.io/en/stable/)
  - **Role:** Password Hashing Library.
  - **Description:** A comprehensive password hashing library that provides secure, adaptive hashing with bcrypt to protect against brute-force attacks.

---

### **Background Tasks & Scheduling: Scalable & Reliable**

Robust infrastructure for handling asynchronous tasks, scheduled jobs, and background processing with built-in monitoring.

- [**Celery**](https://docs.celeryq.dev/en/stable/)
  - **Role:** Distributed Task Queue.
  - **Description:** A powerful, distributed task queue capable of handling millions of tasks per minute with reliable execution and horizontal scaling.
- [**Celery Beat**](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html)
  - **Role:** Periodic Task Scheduler.
  - **Description:** The scheduling component of Celery that handles recurring and cron-like task execution for jobs like data processing and report generation.
- [**Flower**](https://flower.readthedocs.io/en/latest/)
  - **Role:** Celery Monitoring Tool.
  - **Description:** A web-based tool for real-time monitoring and administration of Celery clusters, providing visibility into tasks and workers.

---

### **Deployment & Infrastructure: Linux-Based**

A modern deployment architecture optimized for reliability and performance using automated HTTPS.

- [**Caddy 2.7+**](https://caddyserver.com/docs/)
  - **Role:** Modern Web Server with Automatic HTTPS.
  - **Description:** A powerful web server that automatically provisions and renews TLS certificates, simplifying deployment and reverse proxy configuration.

---

### **Monitoring & Observability: Production-Grade Insights**

A comprehensive monitoring stack providing logs, metrics, and traces for maintaining healthy production applications.

- [**structlog**](https://www.structlog.org/en/stable/)
  - **Role:** Structured Logging for Python.
  - **Description:** A library that enables structured, contextual, and machine-readable logs that integrate seamlessly with modern observability platforms.
- [**Sentry**](https://docs.sentry.io/platforms/python/)
  - **Role:** Application Monitoring and Error Tracking.
  - **Description:** A real-time error tracking and performance monitoring platform that helps developers identify and resolve issues in production.
- [**OpenTelemetry**](https://opentelemetry.io/docs/instrumentation/python/)
  - **Role:** Observability Framework.
  - **Description:** A vendor-neutral framework providing APIs and tooling to collect, process, and export telemetry data (metrics, logs, and traces).

---

### **Package Management: Next-Generation Tooling**

Modern package management that dramatically improves development speed and reliability for both frontend and backend.

- [**pnpm 8+**](https://pnpm.io/motivation) _(Frontend)_
  - **Role:** Fast, Disk Space Efficient Package Manager.
  - **Description:** A performant alternative to npm that reduces disk space usage and provides strict dependency resolution for reliable frontend builds.
- [**uv**](https://docs.astral.sh/uv/) _(Python)_
  - **Role:** Ultra-Fast Python Package and Project Manager.
  - **Description:** A comprehensive Python project and package manager written in Rust that provides 10-100x faster operations than traditional tools.
