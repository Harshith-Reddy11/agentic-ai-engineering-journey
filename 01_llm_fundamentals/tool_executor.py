from tools import TOOL_REGISTRY
import logging

from schemas import (
    ToolCall,
    CalculatorArguments,
    KnowledgeSearchArguments,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s : %(message)s"
)

logger = logging.getLogger(__name__)

TOOL_SCHEMAS = {
    "calculator": CalculatorArguments,
    "knowledge_search": KnowledgeSearchArguments,
}


def execute_tool(tool_call: ToolCall):

    tool_name = tool_call.tool_name
    arguments = tool_call.arguments
    logger.info("Executing tool: %s", tool_name)

    if tool_name not in TOOL_REGISTRY:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}"
        }

    tool = TOOL_REGISTRY[tool_name]
    try:
        if tool_name in TOOL_SCHEMAS:
            schema = TOOL_SCHEMAS[tool_name]
            validated_arguments = schema(**arguments)
            arguments = validated_arguments.model_dump()

        result = tool(**arguments)
        logger.info("Tool execution successful: %s", tool_name)

        return {
            "success": True,
            "result": result
        }

    except Exception as e:
        logger.error("Tool execution failed: %s", e)
        return {
            "success": False,
            "error": str(e)
        }
        
        
if __name__ == "__main__":
    print("\n--- Knowledge Search Validation ---")

    knowledge_call = ToolCall(
        tool_name="knowledge_search",
        arguments={
            "query": "What is an LLM?"
        }
    )

    print(execute_tool(knowledge_call))
    print("\n--- Missing Knowledge Query ---")

    bad_knowledge_call = ToolCall(
        tool_name="knowledge_search",
        arguments={}
    )

    print(execute_tool(bad_knowledge_call))
