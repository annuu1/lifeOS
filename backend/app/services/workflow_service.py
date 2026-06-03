from typing import Dict, Any, List
from telegram import Bot
import os

class WorkflowService:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token

    async def trigger_proactive_actions(self, chat_id: str, extracted_entities: Dict[str, Any]):
        actions = []
        
        # Health Workflow
        for record in extracted_entities.get("health_records", []):
            # Confidence check (assumed high if present for now, but can be scaled)
            if record["status"] == "active":
                actions.append(f"I've noted that you're dealing with {record['condition']}. Have you consulted a doctor yet?")
                actions.append("Would you like me to set reminders for any medicines or hydration?")

        # Asset/Purchase Workflow
        for event in extracted_entities.get("timeline_events", []):
            if "scooter" in event["description"].lower() or "car" in event["description"].lower():
                actions.append(f"Congrats on the new {event['description']}! Should I schedule a reminder for its first service or insurance renewal?")

        # Confidence based Fact validation
        for fact in extracted_entities.get("life_facts", []):
            if fact.get("confidence", 1.0) < 0.7:
                actions.append(f"I think I heard that {fact['fact']}, but I'm not sure. Did I get that right?")

        return actions
