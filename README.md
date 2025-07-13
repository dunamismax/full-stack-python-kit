<p align="center">
  <img src="https://raw.githubusercontent.com/python/cpython/main/Doc/static/py.svg" alt="The Python programming language logo." width="150"/>
</p>

<p align="center">
  <a href="https://github.com/dunamismax/full-stack-python-kit">
    <img src="https://readme-typing-svg.demolab.com/?font=Fira+Code&size=24&pause=1000&color=3776AB&center=true&vCenter=true&width=800&lines=The+Full-Stack+Python+Kit;Official+Reference+Implementation;FastAPI+%2B+Next.js+%2B+SQLModel;Typer%2C+NiceGUI%2C+and+uv;Modern%2C+Performant%2C+and+Beautiful." alt="Typing SVG" />
  </a>
</p>

<p align="center">
  <a href="https://python.org/"><img src="https://img.shields.io/badge/Python-3.11+-3776AB.svg" alt="Python Version"></a>
  <a href="https://img.shields.io/github/license/dunamismax/full-stack-python-kit"><img src="https://img.shields.io/github/license/dunamismax/full-stack-python-kit" alt="License"></a>
  <a href="https://img.shields.io/github/repo-size/dunamismax/full-stack-python-kit"><img src="https://img.shields.io/github/repo-size/dunamismax/full-stack-python-kit" alt="Repo Size"></a>
  <a href="https://github.com/dunamismax/full-stack-python-kit/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
  <a href="https://github.com/dunamismax/full-stack-python-kit/stargazers"><img src="https://img.shields.io/github/stars/dunamismax/full-stack-python-kit" alt="GitHub Stars"></a>
</p>

---

## About This Project

This monorepo is the official reference implementation for **The Full-Stack Python Kit**, a comprehensive architecture for building CLI applications, GUI desktop apps, and full-stack web applications with modern Python.

The primary goal is to provide a structured and scalable environment that combines powerful, battle-tested libraries with modern Python patterns for maximum developer productivity and type safety. The result is a stack that prioritizes rapid development, performance, and long-term maintainability.

---

<details>
<summary><h3>The Full-Stack Python Kit (Click to Expand)</h3></summary>

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

---

### **Authentication & Security: Production-Ready**

A robust security implementation following industry best practices for authentication, authorization, and data protection.

- [**python-jose[cryptography]**](https://python-jose.readthedocs.io/en/latest/)
  - **Role:** JSON Web Token (JWT) Library.
  - **Description:** A JOSE implementation for handling JWT, JWS, and JWK, essential for implementing secure, stateless authentication in web applications.
- [**passlib[bcrypt]**](https://passlib.readthedocs.io/en/stable/)
  - **Role:** Password Hashing Library.
  - **Description:** A comprehensive password hashing library that provides secure, adaptive hashing with bcrypt to protect against brute-force attacks.

---

### **Monitoring & Observability: Production-Grade Insights**

A comprehensive monitoring stack providing logs, metrics, and traces for maintaining healthy production applications.

- [**structlog**](https://www.structlog.org/en/stable/)
  - **Role:** Structured Logging for Python.
  - **Description:** A library that enables structured, contextual, and machine-readable logs that integrate seamlessly with modern observability platforms.
- [**Sentry**](https://docs.sentry.io/platforms/python/)
  - **Role:** Application Monitoring and Error Tracking.
  - **Description:** A real-time error tracking and performance monitoring platform that helps developers identify and resolve issues in production.

</details>

---

<p align="center">
  <img src="https://user-images.githubusercontent.com/7955140/192058087-0ad5d609-52c5-4b36-9ae1-29ac39348c47.png" alt="Python Gopher." width="150"/>
</p>

## Applications Included

This monorepo includes three fully-featured applications demonstrating different aspects of modern Python development:

### 🖥️ **CLI Application** (Typer + Rich)
**Location:** `apps/cli/main.py`

A comprehensive command-line interface showcasing:
- **File Operations**: List directories, read files with syntax highlighting
- **API Testing**: Make HTTP requests with beautiful output formatting
- **System Information**: Display system stats and environment variables
- **Rich Output**: Colors, tables, progress bars, and interactive elements

```bash
# Example usage
just run-cli hello "World" --count 3
just run-cli file list --details
just run-cli api get https://httpbin.org/json --pretty
```

### 🎮 **GUI Desktop Application** (NiceGUI)
**Location:** `apps/gui/main.py`

A modern desktop application with dark theme featuring:
- **Dashboard**: System overview and quick actions
- **System Monitor**: Real-time system information
- **API Tester**: Interactive HTTP request testing
- **File Explorer**: Navigate and browse file system
- **Dark Theme**: Beautiful, responsive interface

```bash
# Run the desktop app
just run-gui
```

### 🌐 **Full-Stack Web Application** (FastAPI + Next.js)

#### **Backend** (`apps/webapp/backend/`)
A production-ready REST API with:
- **Authentication**: JWT-based login/register system
- **Task Management**: CRUD operations with filtering and search
- **Note Taking**: Rich text notes with tagging system
- **Real-time Features**: WebSocket support for live updates
- **API Documentation**: Automatic interactive docs at `/api/v1/docs`
- **Database**: PostgreSQL with async SQLModel ORM
- **Testing**: Comprehensive test suite with fixtures

#### **Frontend** (`apps/webapp/frontend/`)
A modern React application featuring:
- **Dark Theme**: Beautiful Material-UI interface
- **Authentication**: Login/register forms with validation
- **Dashboard**: Stats, quick actions, and recent activity
- **Real-time Updates**: WebSocket integration for live data
- **Type Safety**: Full TypeScript integration
- **State Management**: Zustand for global state

```bash
# Run the full web application
just dev  # Starts both backend and frontend
```

---

## Getting Started

### Prerequisites

- **Python 3.11+**
- **Node.js 18+ & pnpm**
- **PostgreSQL 15+**
- **Redis 7+**
- **uv** (Python package manager)
- **just** (Command runner)

### Installation & Usage

1. **Clone the repository:**

   ```bash
   git clone https://github.com/dunamismax/full-stack-python-kit.git
   cd full-stack-python-kit
   ```

2. **Setup Development Environment:**
   This one-time command installs all Python dependencies and development tools using uv.

   ```bash
   just setup
   ```

3. **Install Frontend Dependencies:**
   Navigate to the frontend directory and install Node.js dependencies.

   ```bash
   cd apps/webapp/frontend
   pnpm install
   cd ../../..
   ```

4. **Configure Your Environment:**
   Create environment configuration for database and service URLs.

   ```bash
   cp .env.example .env
   # Edit .env with your database and Redis URLs
   ```

5. **Setup Database:**
   Create the database and run migrations.

   ```bash
   createdb fspk_db  # Create PostgreSQL database
   just db-upgrade   # Run database migrations
   ```

6. **Start Development:**
   Launch all services for full-stack development.

   ```bash
   just dev
   ```

   This starts:
   - FastAPI backend at `http://localhost:8000`
   - Next.js frontend at `http://localhost:3000`
   - API documentation at `http://localhost:8000/api/v1/docs`

---

## Just Commands

[Just](https://github.com/casey/just) is used to automate common development tasks. You can list all available commands by running `just --list`.

### Primary Workflow Commands

- `just dev`: **(Primary)** Starts all services for full-stack development
- `just setup`: Sets up the complete development environment
- `just check`: Runs all quality checks (lint, typecheck)
- `just test-cov`: Runs tests with coverage report
- `just format`: Formats all code with ruff

### Application Commands

- **CLI Application**
  - `just run-cli [args]`: Run the CLI application with arguments
- **GUI Application**
  - `just run-gui`: Launch the desktop GUI application
- **Web Application**
  - `just run-webapp-dev`: Start FastAPI backend only
  - `just run-webapp-frontend`: Start Next.js frontend only

### Development Tools

- **Code Quality**
  - `just lint`: Run ruff linter
  - `just typecheck`: Run mypy type checker
  - `just format`: Format code with ruff
- **Testing**
  - `just test`: Run pytest test suite
  - `just test-cov`: Run tests with HTML coverage report
- **Database**
  - `just db-upgrade`: Apply database migrations
  - `just db-downgrade`: Rollback last migration
  - `just db-revision "message"`: Create new migration

### Background Services

- `just celery-worker`: Start Celery task worker
- `just celery-beat`: Start Celery scheduler
- `just flower`: Start Flower monitoring dashboard

### Maintenance

- `just clean`: Remove build artifacts and cache files
- `just update`: Update all dependencies
- `just info`: Display project information

---

## Project Structure

```
full-stack-python-kit/
├── apps/                           # Applications
│   ├── cli/                        # CLI application (Typer)
│   │   └── main.py                 # Entry point with Rich output
│   ├── gui/                        # Desktop GUI (NiceGUI)
│   │   └── main.py                 # Cross-platform desktop app
│   └── webapp/                     # Full-stack web application
│       ├── backend/                # FastAPI backend
│       │   ├── app/                # Application logic
│       │   │   ├── routes/         # API route handlers
│       │   │   ├── api.py          # Router configuration
│       │   │   └── monitoring.py   # Observability setup
│       │   ├── migrations/         # Alembic database migrations
│       │   ├── main.py            # FastAPI application
│       │   └── alembic.ini        # Migration configuration
│       └── frontend/               # Next.js frontend
│           ├── src/               # TypeScript source code
│           │   ├── app/           # Next.js app router
│           │   ├── components/    # React components
│           │   ├── lib/           # Utilities and hooks
│           │   └── store/         # State management
│           ├── package.json       # Node.js dependencies
│           └── *.config.js        # Build configuration
├── packages/                       # Shared Python packages
│   ├── core/                      # Core utilities
│   │   ├── config.py              # Pydantic settings
│   │   └── logging.py             # Structured logging
│   ├── auth/                      # Authentication utilities
│   │   ├── auth.py                # JWT handling
│   │   └── password.py            # Password hashing
│   └── database/                  # Database layer
│       ├── models.py              # SQLModel definitions
│       └── session.py             # Database sessions
├── tests/                          # Test suite
│   ├── unit/                      # Unit tests
│   ├── integration/               # Integration tests
│   ├── e2e/                       # End-to-end tests
│   └── conftest.py                # Pytest configuration
├── pyproject.toml                  # Python project config
├── justfile                        # Development commands
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

---

## Features Showcase

### 🔐 **Authentication System**
- JWT-based stateless authentication
- Secure password hashing with bcrypt
- User registration and login
- Protected routes and middleware
- Token refresh mechanism

### 📋 **Task Management**
- Create, read, update, delete tasks
- Priority levels (low, medium, high)
- Due date tracking
- Completion status
- Filter and search capabilities

### 📝 **Note Taking System**
- Rich text note creation
- Tag-based organization
- Full-text search
- Word count statistics
- JSON tag storage

### ⚡ **Real-time Features**
- WebSocket connections
- Live task updates
- Real-time notifications
- Typing indicators
- Connection status monitoring

### 🎨 **Modern UI/UX**
- Dark theme throughout
- Responsive design
- Material-UI components
- Smooth animations
- Accessibility support

### 🔧 **Developer Experience**
- Type safety with TypeScript and mypy
- Hot reloading for rapid development
- Comprehensive testing suite
- Structured logging
- API documentation
- Database migrations

---

## Contributing

Contributions are welcome! Please feel free to fork the repository, create a feature branch, and open a pull request. Make sure to:

1. Follow the existing code style (ruff formatting)
2. Add tests for new functionality
3. Update documentation as needed
4. Run `just check` before submitting

---

### Support My Work

If you find my work on this stack valuable, consider supporting me. It helps me dedicate more time to creating and maintaining open-source projects.

<p align="center">
  <a href="https://coff.ee/dunamismax" target="_blank">
    <img src="https://raw.githubusercontent.com/egonelbre/gophers/master/.thumb/animation/buy-morning-coffee-3x.gif" alt="Buy Me a Coffee" />
  </a>
</p>

---

### Let's Connect

<p align="center">
  <a href="https://twitter.com/dunamismax" target="_blank"><img src="https://img.shields.io/badge/Twitter-%231DA1F2.svg?&style=for-the-badge&logo=twitter&logoColor=white" alt="Twitter"></a>
  <a href="https://bsky.app/profile/dunamismax.bsky.social" target="_blank"><img src="https://img.shields.io/badge/Bluesky-blue?style=for-the-badge&logo=bluesky&logoColor=white" alt="Bluesky"></a>
  <a href="https://reddit.com/user/dunamismax" target="_blank"><img src="https://img.shields.io/badge/Reddit-%23FF4500.svg?&style=for-the-badge&logo=reddit&logoColor=white" alt="Reddit"></a>
  <a href="https://discord.com/users/dunamismax" target="_blank"><img src="https://img.shields.io/badge/Discord-dunamismax-7289DA.svg?style=for-the-badge&logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://signal.me/#p/+dunamismax.66" target="_blank"><img src="https://img.shields.io/badge/Signal-dunamismax.66-3A76F0.svg?style=for-the-badge&logo=signal&logoColor=white" alt="Signal"></a>
</p>

---

<p align="center">
    <img src="https://raw.githubusercontent.com/matplotlib/matplotlib/main/doc/_static/logo2_compressed.svg" alt="Python Data Science" width="200"/>
</p>

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.