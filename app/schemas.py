# app/schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime,date

# ----------------------------------------------------------------------
# 1. SUPERVISOR SCHEMAS (FIXED: Added photo_url)
# ----------------------------------------------------------------------

class SupervisorBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    assigned_plots: List[str] = Field(default_factory=list)
    field_manager_id: Optional[str] = None 
    photo_url: Optional[str] = None # <<< ADDED for S3 URL
    
class SupervisorCreate(SupervisorBase):
    pass 

class Supervisor(SupervisorBase):
    id: str
    class Config:
        from_attributes = True 

class SupervisorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    assigned_plots: Optional[List[str]] = None
    photo_url: Optional[str] = None # <<< ADDED for S3 URL


# ----------------------------------------------------------------------
# 2. TASK SCHEMAS (NO CHANGE)
# ----------------------------------------------------------------------

class TaskBase(BaseModel):
    type: str
    task: str
    plot: str
    supervisor_id: str
    status: str = "Pending"
    due_date: Optional[date] = None
    required_item_id: Optional[str] = None 
    required_quantity: Optional[float] = None

class TaskCreate(TaskBase):
    pass 

class Task(TaskBase):
    id: str
    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    status: str


# ----------------------------------------------------------------------
# 3. INVENTORY SCHEMAS (NO CHANGE)
# ----------------------------------------------------------------------

class InventoryItemBase(BaseModel):
    item: str
    category: str
    stock: float
    unit: str
    threshold: float = 0 
    last_updated: Optional[datetime] = None

class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItem(InventoryItemBase):
    id: str
    class Config:
        from_attributes = True

class InventoryUpdate(BaseModel):
    stock_change: Optional[float] = None
    new_stock: Optional[float] = None


# ----------------------------------------------------------------------
# 4. UTILITY & PLOT SCHEMAS (NO CHANGE)
# ----------------------------------------------------------------------

class CurrentUser(BaseModel):
    user_id: str = Field(..., description="The unique ID of the authenticated user.")
    role: str = Field(..., description="The role of the user (FarmManager, FieldManager, Supervisor).")

class SupervisorPerformance(BaseModel):
    supervisor_id: str
    total_tasks: int
    completed_tasks: int
    completion_percentage: float
    name: Optional[str] = None

class Geolocation(BaseModel):
    latitude: float
    longitude: float

class PlotBase(BaseModel):
    name: str
    plot_number: str 
    geolocation: Geolocation
    supervisor_id: Optional[str] = None
    field_manager_id: Optional[str] = None

class PlotCreate(PlotBase):
    pass

class Plot(PlotBase):
    id: str
    class Config:
        from_attributes = True