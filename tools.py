from langchain_core.tools import tool

# This is the simple dictionary database required by the project
fake_db = {
    "capital of france": "Paris",
    "capital of india": "New Delhi",
    "founder of python": "Guido van Rossum",
    "current year": "2025"
}

@tool
def search_tool(query: str):
    """
    Useful for factual questions. Looks up information in a local dictionary.
    Input should be a simple search query like 'capital of india'.
    """
    # Simple dictionary lookup (case insensitive)
    return fake_db.get(query.lower(), "I couldn't find that information in my database.")