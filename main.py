
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()
timetable = []

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to ["http://localhost:8000"] etc.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    message: str

@app.post("/upload-timetable/")
async def upload_timetable(file: UploadFile = File(...)):
    global timetable
    content = await file.read()
    timetable = json.loads(content)
    return {"message": "Timetable uploaded and loaded successfully."}

@app.post("/chat/")
def chat(query: Query):
    msg = query.message.lower()
    results = []

    for cls in timetable:
        # Match all classes for a given day (collect multiple)
        if cls["day"].lower() in msg:
            results.append(f"{cls['time']}: {cls['subject']} with {cls['faculty']} in {cls['room']}")
        # Match subject directly
        elif cls["subject"].lower() in msg:
            return {
                "reply": f"{cls['subject']} is on {cls['day']} at {cls['time']} in {cls['room']} by {cls['faculty']}"
            }
        # Match time-based queries like "12" or "10:00"
        elif cls["time"].split(":")[0] in msg or cls["time"][:2] in msg:
            return {
                "reply": f"At {cls['time']}, you have {cls['subject']} in {cls['room']} with {cls['faculty']} on {cls['day']}"
            }

    if results:
        return {
            "reply": f"Here are your classes on {query.message.title()}:\n" + "\n".join(results)
        }

    return {"reply": "Sorry, I couldn’t find anything relevant."}




