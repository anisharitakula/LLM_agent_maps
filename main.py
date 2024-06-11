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
        "<h1>Welcome to the LLM maps&calculator API</h1>"
        "<div>"
        "Check the docs: <a href='/process_text'>here</a>"
        "</div>"
        "</body>"
        "</html>"
    )

    return HTMLResponse(content=body)

@app.post("/process_text")
async def process_text(input_text):
    # Replace this with your actual processing logic
    processed_text = Stream_agent(input_text)  # Example processing: convert to uppercase
    return processed_text

if __name__ == "__main__":
    uvicorn.run(app,host="localhost",port=8001)