# AI App Generator

An AI-powered application generator and deployment platform that leverages artificial intelligence to create, manage, and deploy applications with minimal effort.

## Features

- **AI-Powered Code Generation**: Generate application code using advanced AI models
- **Project Management**: Create, manage, and organize your AI-generated projects
- **Version Control**: Track project versions and changes
- **File Management**: Upload and manage project files
- **Deployment**: Deploy generated applications to production
- **Authentication**: Secure user authentication with JWT tokens
- **Rate Limiting**: Protect APIs with intelligent rate limiting
- **Audit Logging**: Track all user actions and changes
- **RESTful API**: Comprehensive REST API for all operations

## Technology Stack

- **Backend**: FastAPI, SQLAlchemy, Python 3.9+
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: JWT with Passlib
- **AI Integration**: OpenAI API
- **Rate Limiting**: slowapi
- **Caching**: Redis (optional)
- **Testing**: pytest, pytest-asyncio

## Prerequisites

- Python 3.9 or higher
- pip or poetry
- Redis (optional, for caching)
- OpenAI API key (for AI features)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-app-generator
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
```

5. Configure environment variables in `.env`: