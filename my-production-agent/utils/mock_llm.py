"""Mock LLM module - provides canned responses for development."""


MOCK_RESPONSES = {
    "hello": "Hello! How can I help you today?",
    "hi": "Hi there! What can I assist you with?",
    "hey": "Hey! I'm here to help.",
    "docker": "Docker is a containerization platform that packages your application with its dependencies into a container, making it easy to deploy and run anywhere.",
    "kubernetes": "Kubernetes (K8s) is an open-source container orchestration platform that automates deployment, scaling, and management of containerized applications.",
    "api": "An API (Application Programming Interface) allows different software applications to communicate with each other. REST APIs use HTTP methods like GET, POST, PUT, DELETE.",
    "database": "A database is an organized collection of structured information stored electronically. Common types include SQL (PostgreSQL, MySQL) and NoSQL (MongoDB, Redis).",
    "redis": "Redis is an in-memory data structure store used as a database, cache, and message broker. It supports strings, hashes, lists, sets, and more.",
    "python": "Python is a high-level, interpreted programming language known for its readable syntax and versatility in web development, data science, AI, and more.",
    "fastapi": "FastAPI is a modern Python web framework for building APIs with high performance, automatic OpenAPI documentation, and type validation using Pydantic.",
    "nginx": "Nginx is a web server that can also act as a reverse proxy, load balancer, and HTTP cache. It's known for high performance and low memory usage.",
    "deployment": "Deployment is the process of making your application available in a production environment. Best practices include: containers, CI/CD, monitoring, and rolling updates.",
    "cloud": "Cloud computing provides on-demand computing resources over the internet. Major providers include AWS, GCP, and Azure, offering services like compute, storage, and AI.",
    "devops": "DevOps combines development and operations to shorten the development lifecycle, improve reliability, and enable continuous delivery through automation.",
    "microservices": "Microservices is an architectural style that structures an application as a collection of loosely coupled, independently deployable services.",
}


def get_mock_response(question: str) -> str:
    """
    Get a mock LLM response based on keywords in the question.

    Args:
        question: The user's question

    Returns:
        A mock response string
    """
    question_lower = question.lower()

    for keyword, response in MOCK_RESPONSES.items():
        if keyword in question_lower:
            return response

    return f"You asked: '{question}'. This is a mock AI response. In production, this would call OpenAI GPT-4, Anthropic Claude, or another LLM API."
