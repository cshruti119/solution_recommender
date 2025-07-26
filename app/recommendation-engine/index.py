from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from complaint_analyzer import analyze_complaint
import os
import uvicorn

app = FastAPI()

REASON_JSON_PATH = os.path.join(os.path.dirname(__file__), 'reason_type_mapping.json')

@app.post('/analyze-complaint')
async def analyze_complaint_api(request: Request):
    data = await request.json()
    sentence = data.get('sentence', '')
    result = analyze_complaint(sentence, REASON_JSON_PATH)
    return JSONResponse(content=result)

if __name__ == '__main__':
    uvicorn.run("index:app", host="0.0.0.0", port=8771, reload=True)
