from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pika
import json
import uuid
from datetime import datetime
from config.settings import settings

router = APIRouter()

class ScrapingTriggerRequest(BaseModel):
    url: str = None
    priority: int = 1

class ScrapingTriggerResponse(BaseModel):
    success: bool
    message: str
    event_id: str

def get_rabbitmq_connection():
    connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
    return connection

@router.post("/trigger-scraping", response_model=ScrapingTriggerResponse)
async def trigger_scraping(request: ScrapingTriggerRequest):
    try:
        event_id = str(uuid.uuid4())

        event_data = {
            "event_id": event_id,
            "event_type": "start_scraping",
            "timestamp": datetime.utcnow().isoformat(),
            "payload": {
                "url": request.url,
                "priority": request.priority
            }
        }

        connection = get_rabbitmq_connection()
        channel = connection.channel()

        channel.queue_declare(queue='scraping_events', durable=True)

        channel.basic_publish(
            exchange='',
            routing_key='scraping_events',
            body=json.dumps(event_data),
            properties=pika.BasicProperties(
                delivery_mode=2,
                message_id=event_id
            )
        )

        connection.close()

        return ScrapingTriggerResponse(
            success=True,
            message="Scraping event triggered successfully",
            event_id=event_id
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to trigger scraping event: {str(e)}"
        )