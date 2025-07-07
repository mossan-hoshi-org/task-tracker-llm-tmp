# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Task Tracker Desktop Application** built with Python and Tkinter. The app tracks work time with task switching capabilities and exports results in Markdown format. It integrates with Google Gemini API for automatic task categorization.

## Development Philosophy

### Test-Driven Development (TDD)
All features must be developed using TDD methodology:
1. Write failing test first
2. Write minimal code to make test pass
3. Refactor while keeping tests green

### Assertion-Based Design
- Use assertions liberally to document and enforce preconditions, postconditions, and invariants
- Assertions should be used for internal consistency checks, not for input validation
- Example: `assert self.is_running, "Timer must be running to pause"`

### No Comments or Docstrings Policy
- **NO comments** in code (except TODO/NOTE comments)
- **NO docstrings** in any functions, classes, or modules
- Code should be self-documenting through:
  - Clear variable and function names
  - Small, focused functions
  - Descriptive assertions
- Allowed exceptions:
  - `# TODO: <specific task>`
  - `# NOTE: <critical information>`

## Development Commands

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create new project with uv
uv init

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# Install dependencies
uv pip install -r requirements.txt

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=html

# Run the application
uv run python src/main.py
```

## Architecture & Key Components

### Core Technologies
- **Python 3.12+** - Main programming language
- **Tkinter** - GUI framework (built-in, no installation needed)
- **Google Gemini API** - For AI-powered task categorization
- **Markdown** - Output format for summaries
- **pytest** - Testing framework
- **uv** - Fast Python package manager

### Project Structure with TDD
```
task-tracker-llm/
├── src/
│   ├── main.py              # Application entry point
│   ├── models/
│   │   └── session.py       # Session management with assertions
│   ├── services/
│   │   └── gemini_client.py # Gemini API integration
│   ├── ui/
│   │   ├── main_screen.py   # Main tracking interface
│   │   └── summary_screen.py # Summary view
│   └── utils/
│       └── markdown.py      # Markdown formatting
├── tests/
│   ├── test_models/
│   │   └── test_session.py
│   ├── test_services/
│   │   └── test_gemini_client.py
│   ├── test_ui/
│   │   ├── test_main_screen.py
│   │   └── test_summary_screen.py
│   └── test_utils/
│       └── test_markdown.py
├── pyproject.toml           # Project configuration
└── requirements.txt         # Dependencies
```

## TDD Workflow

### 1. Start with a Test
```python
# tests/test_models/test_session.py
def test_session_start_creates_new_session():
    session = Session("Task 1")
    session.start()

    assert session.is_running
    assert session.start_time is not None
    assert session.task_name == "Task 1"
```

### 2. Implement with Assertions (No Comments/Docstrings)
```python
# src/models/session.py
class Session:
    def __init__(self, task_name: str):
        assert task_name, "Task name cannot be empty"
        self.task_name = task_name
        self.is_running = False
        self.start_time = None

    def start(self):
        assert not self.is_running, "Session is already running"
        self.is_running = True
        self.start_time = datetime.now()
```

### 3. Test Preconditions and Postconditions
```python
# tests/test_models/test_session.py
def test_session_pause_requires_running_session():
    session = Session("Task 1")

    with pytest.raises(AssertionError, match="Session must be running"):
        session.pause()
```

### Key Functional Requirements

1. **Session Management** (FR-01, FR-02)
   - Track task start/stop times with automatic task switching
   - Store sessions in memory during runtime

2. **Time Display** (FR-03)
   - Real-time elapsed time in hh:mm:ss format
   - 1-second update interval using Tkinter's `after()` method

3. **Task Controls** (FR-04, FR-05)
   - Pause/Resume functionality with cumulative time tracking
   - Stop button to end session and show summary

4. **Summary Features** (FR-06, FR-07, FR-08)
   - Markdown-formatted output with task durations
   - AI categorization via Gemini API
   - Clipboard copy functionality

5. **Error Handling** (FR-10)
   - Exception handling with user-friendly dialog boxes
   - Safe API key management via environment variables

## Development Approach with TDD

When implementing features using TDD:

1. **Red Phase**: Write a failing test that defines the expected behavior
2. **Green Phase**: Write minimal code to make the test pass
3. **Refactor Phase**: Improve code quality while keeping tests green
4. **Assertion Design**: Add assertions for all critical invariants

### Example TDD Implementation Order
1. Test and implement Session model with basic start/stop
2. Test and implement pause/resume functionality
3. Test and implement task switching logic
4. Test and implement time calculation
5. Test and implement Markdown export
6. Create UI components with manual testing
7. Test and implement Gemini API integration

## Assertion-Based Design Guidelines

### When to Use Assertions
- **Preconditions**: Validate method inputs and object state
- **Postconditions**: Ensure methods produce expected results
- **Invariants**: Maintain object consistency throughout lifecycle

### Assertion Examples
```python
class TaskTracker:
    def switch_task(self, new_task: str):
        assert new_task, "New task name cannot be empty"
        assert self.current_session, "No active session to switch from"

        old_session = self.current_session
        old_session.stop()
        self.current_session = Session(new_task)
        self.current_session.start()

        assert self.current_session.task_name == new_task, "Task switch failed"
        assert self.current_session.is_running, "New session must be running"
```

### What NOT to Assert
- User input validation (use exceptions instead)
- External API responses (handle with try/except)
- File I/O operations (use proper error handling)

## Important Considerations

- **No File Persistence**: The app doesn't save data to disk; results are only copied to clipboard
- **API Key Security**: Never hardcode API keys; use environment variables or config files
- **Task Switching Logic**: Starting a new task automatically stops the previous one
  - Assert that only one session can be running at a time
- **Timezone Handling**: Consider timezone issues for accurate time tracking
- **Type Hints**: Add type hints to all functions for better code clarity
- **Test Coverage**: Maintain >90% test coverage for all business logic
