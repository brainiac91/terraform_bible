from fastapi import APIRouter, HTTPException
import json
import os

router = APIRouter(
    prefix="/api/terraform",
    tags=["terraform"]
)

TERRAFORM_DIR = "/app/terraform_data"
STATE_FILE = os.path.join(TERRAFORM_DIR, "terraform.tfstate")

@router.get("/state")
async def get_terraform_state():
    if not os.path.exists(STATE_FILE):
        return {"error": "State file not found. Have you run 'terraform apply'?"}
    
    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
        return state
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/resources")
async def get_resources():
    """Simplified view of resources for the UI"""
    if not os.path.exists(STATE_FILE):
        return []
    
    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
        
        resources = []
        if "resources" in state:
            for res in state["resources"]:
                resources.append({
                    "type": res.get("type"),
                    "name": res.get("name"),
                    "provider": res.get("provider"),
                    "instances": len(res.get("instances", []))
                })
        return resources
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
