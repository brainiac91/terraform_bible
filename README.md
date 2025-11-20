# The Terraform Bible

A comprehensive, interactive DevOps learning platform designed to take students from Zero to Hero in Infrastructure as Code using Terraform.

## Overview

The Terraform Bible is a web application that provides a structured learning path for mastering Terraform. It features an interactive dashboard, chapter-based lessons, quizzes, flashcards, and practical challenges. The application is built to track student progress and provide a gamified learning experience.

## Features

-   **Student Dashboard**: Track your course progress, XP, and daily streaks.
-   **Interactive Lessons**: Markdown-based chapters covering everything from basic setup to advanced HCL patterns.
-   **Knowledge Checks**: Quizzes to test your understanding of each chapter.
-   **Flashcards**: Study key terms and concepts.
-   **God Mode Challenges**: Practical coding challenges with hints and solutions.
-   **State Visualizer**: (Experimental) Tools to visualize Terraform state.
-   **Dark Mode**: Fully supported dark mode for late-night coding sessions.

## Tech Stack

-   **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
-   **Frontend**: HTML5, [TailwindCSS](https://tailwindcss.com/), JavaScript
-   **Templating**: Jinja2
-   **Content**: Markdown
-   **Infrastructure**: Docker, Terraform

## Getting Started

### Prerequisites

-   Python 3.9+
-   `pip` (Python Package Manager)

### Installation

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd antigravity
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r app/requirements.txt
    ```

3.  **Run the Application**
    ```bash
    cd app
    python main.py
    ```
    Or using uvicorn directly:
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

4.  **Access the App**
    Open your browser and navigate to `http://localhost:8000`.

## Project Structure

```
antigravity/
├── app/
│   ├── content/        # Course content (chapters, assets)
│   ├── routers/        # API routes (bible, terraform)
│   ├── templates/      # HTML templates (Jinja2)
│   ├── main.py         # Application entry point
│   └── requirements.txt
├── terraform/          # Terraform configuration
└── Dockerfile          # Container definition
```

## License

This project is open source and available under the [MIT License](LICENSE).
