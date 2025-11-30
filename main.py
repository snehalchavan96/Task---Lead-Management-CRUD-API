
from fastapi import FastAPI, HTTPException, Query, Path
from typing import Optional, List, Dict

from models import Lead, LeadCreate, LeadUpdate, LeadType
from database import leads_db, get_next_lead_id

app = FastAPI(title="Lead Management CRUD API")


# 1. Create Lead
@app.post("/api/leads", status_code=201, response_model=Lead)
def create_lead(lead_in: LeadCreate):
    # Check duplicate email
    for lead in leads_db.values():
        if lead.email.lower() == lead_in.email.lower():
            raise HTTPException(
                status_code=400,
                detail="A lead already exists with this email",
            )

    new_id = get_next_lead_id()
    lead = Lead(id=new_id, **lead_in.dict())
    leads_db[new_id] = lead
    return lead


# 2. Get All Leads with pagination + filters
@app.get("/api/leads")
def get_all_leads(
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    lead_type: Optional[LeadType] = Query(None, description="Filter by lead type"),
    city: Optional[str] = Query(None, description="Filter by city (exact match)"),
):
    # Convert dict -> list
    leads_list = list(leads_db.values())

    # Apply filters
    if lead_type is not None:
        leads_list = [l for l in leads_list if l.lead_type == lead_type]
    if city is not None:
        leads_list = [l for l in leads_list if (l.city or "").lower() == city.lower()]

    total = len(leads_list)

    # Pagination
    start = (page - 1) * limit
    end = start + limit
    paginated = leads_list[start:end]

    return {
        "items": paginated,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit if total > 0 else 0,
    }


# 3. Get Single Lead
@app.get("/api/leads/{id}", response_model=Lead)
def get_lead_by_id(id: int = Path(..., ge=1)):
    if id not in leads_db:
        raise HTTPException(status_code=404, detail="Lead not found")
    return leads_db[id]


# 4. Update Lead (only provided fields)
@app.put("/api/leads/{id}", response_model=Lead)
def update_lead(id: int, updated: LeadUpdate):
    if id not in leads_db:
        raise HTTPException(status_code=404, detail="Lead not found")

    existing = leads_db[id]

    # If email is being updated, check duplicate
    if updated.email is not None:
        for other_id, lead in leads_db.items():
            if other_id != id and lead.email.lower() == updated.email.lower():
                raise HTTPException(
                    status_code=400,
                    detail="Another lead already exists with this email",
                )

    # Update only fields that are provided (not None)
    update_data = updated.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing, field, value)

    leads_db[id] = existing
    return existing


# 5. Delete Lead
@app.delete("/api/leads/{id}", status_code=200)
def delete_lead(id: int):
    if id not in leads_db:
        raise HTTPException(status_code=404, detail="Lead not found")
    del leads_db[id]
    return {"message": "Lead deleted successfully"}
