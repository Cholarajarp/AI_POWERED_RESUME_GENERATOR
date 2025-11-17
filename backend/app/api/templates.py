from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from ..db import crud

router = APIRouter()

class TemplateCreate(BaseModel):
    name: str
    description: str
    type: str  # "cover_letter", "linkedin", "ats_optimization"
    prompt: str
    category: str = "default"

class TemplateOut(BaseModel):
    id: int
    name: str
    description: str
    type: str
    category: str
    is_premium: bool

@router.get("/templates", response_model=List[TemplateOut])
async def list_templates(category: str = None):
    """List available AI templates"""
    # TODO: implement fetching templates from DB
    templates = [
        {
            "id": 1,
            "name": "Professional Cover Letter",
            "description": "Generate a professional cover letter tailored to the job",
            "type": "cover_letter",
            "category": "standard",
            "is_premium": False
        },
        {
            "id": 2,
            "name": "LinkedIn Summary Generator",
            "description": "Create an engaging LinkedIn profile summary",
            "type": "linkedin",
            "category": "standard",
            "is_premium": False
        },
        {
            "id": 3,
            "name": "ATS Optimization Pro",
            "description": "Optimize resume for Applicant Tracking Systems",
            "type": "ats_optimization",
            "category": "premium",
            "is_premium": True
        },
        {
            "id": 4,
            "name": "Executive Summary",
            "description": "Write an executive summary for your resume",
            "type": "cover_letter",
            "category": "premium",
            "is_premium": True
        },
    ]
    return templates

class GenerateRequest(BaseModel):
    template_type: str
    resume_content: str
    job_description: str = None
    additional_context: str = None

class GenerateResponse(BaseModel):
    generated_content: str
    tokens_used: int
    template_type: str

@router.post("/templates/generate", response_model=GenerateResponse)
async def generate_from_template(request: GenerateRequest):
    """Generate content using AI templates"""
    # TODO: implement calling AI service with template-specific prompts
    
    prompts = {
        "cover_letter": """Generate a professional cover letter based on the resume and job description provided.
The cover letter should be compelling, personalized, and highlight relevant skills.""",
        
        "linkedin": """Create an engaging LinkedIn profile summary (2000 characters max) based on the resume.
Make it professional, impactful, and highlight key achievements.""",
        
        "ats_optimization": """Optimize the following resume for Applicant Tracking Systems (ATS).
Improve keyword density, formatting, and structure while maintaining all important information.""",
    }
    
    prompt = prompts.get(request.template_type, "")
    
    return {
        "generated_content": "Generated content will be created based on AI model response",
        "tokens_used": 150,
        "template_type": request.template_type
    }

@router.get("/templates/{template_id}", response_model=TemplateOut)
async def get_template(template_id: int):
    """Get a specific template details"""
    # TODO: fetch from DB
    raise HTTPException(status_code=404, detail="Template not found")
