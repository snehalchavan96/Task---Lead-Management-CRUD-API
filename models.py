
from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional

# Validation fields
PhoneStr = constr(regex=r"^\d{10}$")   # exactly 10 digits
LeadTypeStr = constr(regex=r"^(startup|investor)$")  # only two allowed types


# ---------------------------
# Main Base Model
# ---------------------------
class LeadBase(BaseModel):
    name: str = Field(..., example="Snehal Chavan", max_length=150)
    email: EmailStr = Field(..., example="snehal@example.com")
    phone: PhoneStr = Field(..., example="9876543210")
    lead_type: LeadTypeStr = Field(..., example="startup")  # startup | investor
    city: Optional[str] = Field(None, example="Mumbai", max_length=120)
    company_name: Optional[str] = Field(None, example="Tech Solutions", max_length=200)
    notes: Optional[str] = Field(None, example="Wants more info about services")


# ---------------------------
# Create Lead Model
# ---------------------------
class LeadCreate(LeadBase):
    pass


# ---------------------------
# Update Lead Model (all fields optional)
# ---------------------------
class LeadUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Updated Name", max_length=150)
    email: Optional[EmailStr] = Field(None, example="updated@example.com")
    phone: Optional[PhoneStr] = Field(None, example="9998887776")
    lead_type: Optional[LeadTypeStr] = Field(None, example="investor")
    city: Optional[str] = Field(None, example="Pune", max_length=120)
    company_name: Optional[str] = Field(None, example="Updated Company", max_length=200)
    notes: Optional[str] = Field(None, example="Follow-up scheduled")


# ---------------------------
# Response Model (Lead with ID)
# ---------------------------
class Lead(LeadBase):
    id: int = Field(..., example=1)
