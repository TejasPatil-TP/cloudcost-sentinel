# Contributing to CloudCost Sentinel

Thank you for your interest in contributing to CloudCost Sentinel! We welcome contributions from the community to help make multi-cloud FinOps observability open, accessible, and extensible.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please report any violations to [tejaspatil2626@gmail.com](mailto:tejaspatil2626@gmail.com).

---

## How Can I Contribute?

### Reporting Bugs
* Check the [existing issues](https://github.com/TejasPatil-TP/cloudcost-sentinel/issues) before opening a new issue.
* Provide a clear and descriptive title.
* Include detailed steps to reproduce the behavior, along with expected vs. actual results.
* Include relevant log snippets, error tracebacks, or synthetic CSV schemas (never include proprietary or sensitive billing exports).

### Suggesting Enhancements
* Open an issue with the tag `enhancement`.
* Explain the use case and why this feature would benefit multi-cloud FinOps workflows.
* Detail any provider-specific nuances (AWS CUR, Azure Cost Management, or GCP BigQuery billing).

### Pull Requests
1. Fork the repository and create your branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Follow the development workflow outlined below.
3. Ensure all tests and linting pass locally before pushing.
4. Submit your pull request with a comprehensive summary of changes.

---

## Development Workflow

### Prerequisites
* Python 3.11+
* Node.js 20+ and npm
* Redis (running locally on port 6379 for Celery tasks)

### Backend Setup
1. Navigate to the `backend/` directory:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Initialize database migrations:
   ```bash
   alembic upgrade head
   ```
3. Run the backend test suite:
   ```bash
   python -m pytest tests/
   ```

### Frontend Setup
1. Navigate to the `frontend/` directory:
   ```bash
   cd frontend
   npm install
   ```
2. Verify linting and build:
   ```bash
   npm run lint
   npm run build
   ```

---

## Coding Standards

### Backend (Python / FastAPI)
* Follow PEP 8 guidelines.
* Maintain strict typing and use Pydantic models for request/response serialization.
* Ensure all database operations in tests use the isolated in-memory SQLite pool (`StaticPool`) so developer databases are not modified.
* Avoid vendor lock-in where possible; all cloud adapters must normalize to the shared `BillingRecord` schema.

### Frontend (Next.js / TypeScript / React)
* Use strict TypeScript typing; avoid the use of `any` types.
* Follow Next.js App Router conventions.
* Maintain clean component separation with Tailwind CSS.

---

## Commit Guidelines
* Write clear, concise, and descriptive commit messages following the Conventional Commits specification:
  * `feat:` new features or capabilities
  * `fix:` bug fixes
  * `docs:` documentation improvements
  * `test:` adding or refactoring tests
  * `ci:` CI/CD pipeline changes
  * `refactor:` code adjustments without behavioral change
