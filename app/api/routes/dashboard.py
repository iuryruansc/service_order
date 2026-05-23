from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_db
from app.services.dashboard_service import get_dashboard_data
from app.schemas.dashboard import DashboardRead

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/", response_model=DashboardRead)
def get_dashboard(db: Session = Depends(get_db), _authenticated_admin = Depends(get_current_admin)):
    return get_dashboard_data(db)