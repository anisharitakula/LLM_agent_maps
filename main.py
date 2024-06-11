from fastapi import FastAPI
from code.agent import Stream_agent

app=FastAPI()

@app.post("/process_text")
async def process_text(input_text):
    # Replace this with your actual processing logic
    processed_text = Stream_agent(input_text)  # Example processing: convert to uppercase
    return processed_text
