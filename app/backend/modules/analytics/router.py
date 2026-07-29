"""Analytics module routes — import, dashboard, export."""

import csv
import io

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse

from backend.modules.analytics import service
from backend.modules.analytics.models import ImportResponse, DashboardData

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.post("/import")
async def import_data(file: UploadFile = File(...)) -> ImportResponse:
    """Import CSV/Excel analytics data."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename")
    if not file.filename.endswith((".csv", ".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Only CSV and Excel files supported")
    content = await file.read()
    if len(content) > 50 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large")
    result = await service.import_csv(file.filename, content)
    return ImportResponse(**result)


@router.get("/dashboard")
async def dashboard_data() -> DashboardData:
    """Get aggregated analytics for dashboard."""
    data = await service.get_dashboard_data()
    return DashboardData(**data)


@router.get("/export")
async def export_data() -> StreamingResponse:
    """Export analytics data as CSV."""
    data = await service.export_data()
    if not data:
        raise HTTPException(status_code=404, detail="No data to export")

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=analytics-export.csv"},
    )
