from fastapi import APIRouter, HTTPException, Query, Body, Path, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from modules.eduzaa_skill_up_agent_cluster.router import router as skill_up_router
# Create a router instance
router = APIRouter(
    prefix="/api/openai",
)
router.include_router(skill_up_router)
