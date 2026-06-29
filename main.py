
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
import asyncio
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PulsePitch AI Streaming Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


sentiment_model = None

@app.on_event("startup")
async def load_model():
    global sentiment_model
    logger.info("Loading RoBERTa AI Model (This might take a minute to download on first run)...")
    e
    sentiment_model = pipeline(
        "sentiment-analysis", 
        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
        tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest"
    )
    logger.info("✅ AI Model successfully loaded and ready for streaming!")

# Simulated Live Data Stream (In a real company, this would be a Twitter API or Kafka stream)
MOCK_LIVE_STREAM = [
    {"id": 1, "text": "Great pass by the midfielder, looking sharp today."},
    {"id": 2, "text": "The atmosphere in the stadium is absolutely electric!"},
    {"id": 3, "text": "Decent defense, but we need to push forward more."},
    {"id": 4, "text": "I love this team, what a beautiful style of play."},
    # --- SUDDEN RED CARD / VAR CONTROVERSY ---
    {"id": 5, "text": "ARE YOU BLIND REFEREE??? THAT WAS NEVER A FOUL! 🤬"},
    {"id": 6, "text": "Absolute corruption. Worst refereeing I have ever seen in my life."},
    {"id": 7, "text": "DISGUSTING DECISION! THIS MATCH IS RIGGED!!!"},
    {"id": 8, "text": "I'm turning off the TV. This is a disgrace to football."},
    {"id": 9, "text": "Terrible call, totally ruined a fantastic game."},
    # --- GAME CALMS DOWN ---
    {"id": 10, "text": "Well, we have to defend with 10 men now. Come on boys."},
    {"id": 11, "text": "Still proud of the team no matter what happens."}
]

@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("Frontend connected to live stream.")
    
    try:
      
        while True:
            for item in MOCK_LIVE_STREAM:
                text = item["text"]
                
               
                result = sentiment_model(text)[0]
                label = result['label'].lower()
                score = float(result['score'])
                
               
                toxicity_score = score if label == "negative" else (1.0 - score) * 0.1
                is_toxic = bool(toxicity_score > 0.80)
                
               
                payload = {
                    "id": item["id"],
                    "text": text,
                    "label": label,
                    "confidence": score,
                    "toxicity_score": toxicity_score,
                    "is_toxic": is_toxic
                }
                
                
                await websocket.send_json(payload)               
               
                await asyncio.sleep(2)
                
    except WebSocketDisconnect:
        logger.info("Frontend disconnected from stream.")