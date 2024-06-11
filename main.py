from fastapi import FastAPI
from code.agent import Stream_agent
import uvicorn

app=FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the LLM maps agent"}

@app.post("/process_text")
async def process_text(input_text):
    # Replace this with your actual processing logic
    processed_text = Stream_agent(input_text)  # Example processing: convert to uppercase
    return processed_text

if __name__ == "__main__":
    uvicorn.run(app,host="localhost",port=8001)