from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI
import prompts as p
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

# API hívás a "Marketing Mentor" egyéni GPT modellhez
client = OpenAI(api_key=os.getenv("API_KEY"))

class InputData(BaseModel):
    input: str

def buyer_persona(input_data: str):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": p.buyer_persona},
            {"role": "user", "content": f"Készíts nekem egy vevői avatárt a következő információk alapján: {input_data}"}
        ]
    )
    return response.choices[0].message.content.strip()

@app.get('/buyer_persona')
async def create_buyer_persona(input: str):
    if not input:
        raise HTTPException(status_code=400, detail="Input data is required")
    
    try:
        result = buyer_persona(input)
        # return JSONResponse(content={"buyer_persona": result}, status_code=200)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)
