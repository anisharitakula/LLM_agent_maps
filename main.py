from fastapi import FastAPI
from code.agent import Stream_agent
from fastapi.responses import HTMLResponse
import uvicorn

app=FastAPI()

@app.get("/")
async def root():
    """Basic HTML response."""
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Welcome to the LLM Maps & Calculator API</h1>"
        "<div>"
        "Check the docs: <a href='/docs'>here</a>"
        "</div>"
        "</body>"
        "</html>"
    )

    return HTMLResponse(content=body)

@app.post("/query_text")
async def query_text(input_text):
    # Replace this with your actual processing logic
    processed_text = Stream_agent(input_text)  # Example processing: convert to uppercase
    return processed_text

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=5000)