from fastapi import FastAPI
from pydantic import BaseModel
from agent import graph

app = FastAPI(title="AI QA Helper")

class UserRequest(BaseModel):
    question: str
    thread_id: str = "default_user"

@app.post("/chat")
def chat_endpoint(req: UserRequest):
    # Config for memory
    config = {"configurable": {"thread_id": req.thread_id}}

    # Run the agent
    response = graph.invoke({"messages": [("user", req.question)]}, config=config)

    # Extract last message
    bot_response = response["messages"][-1].content
    return {"response": bot_response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)