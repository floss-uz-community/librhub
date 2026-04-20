from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.moderation import ModerationAction, ModerationReport
from app.models.users import User
from app.schemas.moderation import (
    ModerationActionCreate,
    ModerationActionResponse,
    ModerationReportCreate,
    ModerationReportResponse,
    ModerationReportStatusUpdate,
)
from app.api.dependencies import current_user_jwt_dep, pagination_dep

router = APIRouter()

ALLOWED_STATUSES = {"pending", "reviewing", "resolved", "dismissed"}


def _require_staff(current_user: User):
    if not (current_user.is_staff or current_user.is_superuser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff access required.",
        )


@router.post("/reports/", response_model=ModerationReportResponse, status_code=201)
async def create_report(
    body: ModerationReportCreate,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    report = ModerationReport(
        reporter_user_id=current_user.id,
        target_type=body.target_type,
        target_id=body.target_id,
        reason=body.reason,
        details=body.details,
        status="pending",
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return report


@router.get("/reports/", response_model=list[ModerationReportResponse])
async def list_reports(
    current_user: current_user_jwt_dep,
    pagination: pagination_dep,
    status_filter: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    _require_staff(current_user)
    stmt = select(ModerationReport)
    if status_filter:
        stmt = stmt.where(ModerationReport.status == status_filter)
    stmt = stmt.order_by(ModerationReport.created_at.desc())
    stmt = stmt.offset(pagination.offset).limit(pagination.limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/reports/{report_id}/", response_model=ModerationReportResponse)
async def get_report(
    report_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    _require_staff(current_user)
    result = await db.execute(
        select(ModerationReport).where(ModerationReport.id == report_id)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found.")
    return report


@router.patch("/reports/{report_id}/status", response_model=ModerationReportResponse)
async def update_report_status(
    report_id: int,
    body: ModerationReportStatusUpdate,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    _require_staff(current_user)
    if body.status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Status must be one of: {', '.join(ALLOWED_STATUSES)}",
        )
    result = await db.execute(
        select(ModerationReport).where(ModerationReport.id == report_id)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found.")
    report.status = body.status
    await db.commit()
    await db.refresh(report)
    return report


@router.post(
    "/reports/{report_id}/actions/",
    response_model=ModerationActionResponse,
    status_code=201,
)
async def create_action(
    report_id: int,
    body: ModerationActionCreate,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    _require_staff(current_user)
    result = await db.execute(
        select(ModerationReport).where(ModerationReport.id == report_id)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found.")

    action = ModerationAction(
        report_id=report_id,
        moderator_user_id=current_user.id,
        action_type=body.action_type,
        note=body.note,
    )
    db.add(action)
    await db.commit()
    await db.refresh(action)
    return action


@router.get("/reports/{report_id}/actions/", response_model=list[ModerationActionResponse])
async def list_actions(
    report_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    _require_staff(current_user)
    result = await db.execute(
        select(ModerationReport).where(ModerationReport.id == report_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Report not found.")

    actions_result = await db.execute(
        select(ModerationAction)
        .where(ModerationAction.report_id == report_id)
        .order_by(ModerationAction.created_at)
    )
    return actions_result.scalars().all()
