EXPLAIN_PROMPT = """
You are an AI study assistant.

Explain the following topic to a beginner.
Use simple language and one real-world analogy.

Topic:
{topic}
"""


QUIZ_PROMPT = """
You are an AI study assistant.

Create 5 quiz questions about the following topic.
Start with easy questions and gradually increase the difficulty.

Topic:
{topic}
"""


SUMMARIZE_PROMPT = """
You are an AI study assistant.

Summarize the following text for a student.
Extract the key concepts and important points.

Text:
{text}
"""

ROUTER_PROMPT = """
You are a request classification system.

Classify the user's request into exactly one of these intents:

1. calculator
2. question
3. document_analysis

Return structured data matching the RequestClassification schema.

Rules:

- Use "calculator" when the user wants a mathematical calculation.
- Use "question" when the user wants an explanation or answer to a conceptual question.
- Use "document_analysis" when the user wants to analyze a document.
- Do not invent information.
- Only include fields that are relevant to the user's request.

Examples:

User: Calculate 25 * 8

Output:
{{
    "intent": "calculator",
    "operation": "multiply",
    "number1": 25,
    "number2": 8
}}

User: Explain what an embedding is.

Output:
{{
    "intent": "question",
    "topic": "embeddings"
}}

User: Summarize this document.

Output:
{{
    "intent": "document_analysis",
    "action": "summarize"
}}

User request:
{user_input}
"""
