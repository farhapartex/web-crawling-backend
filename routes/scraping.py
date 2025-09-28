from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pika
import json
import uuid
from datetime import datetime
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class ScrapingTriggerRequest(BaseModel):
    pass

class ScrapingTriggerResponse(BaseModel):
    success: bool
    message: str
    event_id: str

def get_rabbitmq_connection():
    try:
        logger.info(f"Connecting to RabbitMQ: {settings.RABBITMQ_URL}")
        connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
        return connection
    except Exception as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")
        raise

@router.post("/trigger-scraping", response_model=ScrapingTriggerResponse)
async def trigger_scraping():
    try:
        event_id = str(uuid.uuid4())
        logger.info(f"Generated event ID: {event_id}")

        event_data = {
            "event_id": event_id,
            "event_type": "start_scraping",
            "timestamp": datetime.utcnow().isoformat()
        }

        connection = get_rabbitmq_connection()
        channel = connection.channel()

        channel.queue_declare(queue='scraping_events', durable=True)

        logger.info(f"Publishing event to queue: {event_data}")
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
        logger.info(f"Successfully published event {event_id} and closed connection")

        return ScrapingTriggerResponse(
            success=True,
            message="Scraping event triggered successfully",
            event_id=event_id
        )

    except Exception as e:
        logger.error(f"Error in trigger_scraping: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to trigger scraping event: {str(e)}"
        )