from datetime import datetime

knowledge_base = {
    "python": "Python is a high-level programming language commonly used for AI, ML, automation, and web development.",
    "llm": "An LLM is a Large Language Model that can understand and generate human-like text.",
    "agent": "An AI agent is a system that can reason, use tools, and perform tasks.",
}

def calculator(a: float, b: float, operation: str):
    if operation == 'add':
        return a + b
    elif operation == 'subtract':
        return a - b
    elif operation == 'multiply':
        return a * b
    elif operation == 'divide':
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b
    else:
        raise ValueError(f"Unsupported operation: {operation}")
    
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def search_knowledge(query: str):
    query = query.lower()
    for keyword, information in knowledge_base.items():
        if keyword in query:
            return information
    return "No relevant information found"

TOOL_REGISTRY = {
    "calculator" : calculator,
    "current_time" : get_current_time,
    "knowledge_search" : search_knowledge
    
}

if __name__ == "__main__":
    print(TOOL_REGISTRY)

    print(
        TOOL_REGISTRY["calculator"](10, 5, "multiply")
    )

    print(
        TOOL_REGISTRY["current_time"]()
    )

    print(
        TOOL_REGISTRY["knowledge_search"]("What is Python?")
    )