TOOL_DEFINITIONS = [
    {
        "name": "calculator",
        "description": "Perform basic arithmetic calculations.",
        "arguments": {
            "a": "number",
            "b": "number",
            "operation": "add, subtract, multiply, or divide"
        }
    },
    {
        "name": "current_time",
        "description": "Get the current date and time.",
        "arguments": {}
    },
    {
        "name": "knowledge_search",
        "description": "Search the local knowledge base for information.",
        "arguments": {
            "query": "string"
        }
    }
]

if __name__ == "__main__":
    for tool in TOOL_DEFINITIONS:
        print(tool)