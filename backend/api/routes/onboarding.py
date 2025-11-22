"""
Onboarding endpoints.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from backend.api.routes.auth import get_current_user
from backend.database.sleep_db import SleepDatabase

router = APIRouter(prefix="/api/onboarding", tags=["onboarding"])


class OnboardingStatusResponse(BaseModel):
    """Onboarding status response model."""

    is_onboarded: bool
    has_sleep_data: bool
    has_completed_tour: bool
    wearables_configured: bool
    wearable_type: str | None = None
    sleep_goals: str | None = None
    preferences: str | None = None


class OnboardingCompleteRequest(BaseModel):
    """Mark onboarding as complete request model."""

    wearable_type: str | None = None
    sleep_goals: str | None = None
    preferences: str | None = None
    tour_completed: bool = False


class TourRestartRequest(BaseModel):
    """Restart tour request model (currently empty, for future extensibility)."""

    pass


@router.get("/status", response_model=OnboardingStatusResponse)
async def get_onboarding_status(
    current_user: Annotated[str, Depends(get_current_user)]
):
    """
    Get onboarding status for the current user.

    Returns:
        Onboarding status including completion state and configuration
    """
    db = SleepDatabase()
    try:
        onboarding_status = db.get_onboarding_status(current_user)
        if onboarding_status is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return OnboardingStatusResponse(
            is_onboarded=onboarding_status["is_onboarded"],
            has_sleep_data=onboarding_status["has_sleep_data"],
            has_completed_tour=onboarding_status["has_completed_tour"],
            wearables_configured=onboarding_status["wearable_type"] is not None,
            wearable_type=onboarding_status["wearable_type"],
            sleep_goals=onboarding_status["sleep_goals"],
            preferences=onboarding_status["preferences"],
        )
    finally:
        db.close()


@router.post("/complete", status_code=status.HTTP_200_OK)
async def complete_onboarding(
    request: OnboardingCompleteRequest,
    current_user: Annotated[str, Depends(get_current_user)],
):
    """
    Mark onboarding as complete for the current user.

    Args:
        request: Onboarding completion data including wearable type, goals, and preferences

    Returns:
        Success message
    """
    db = SleepDatabase()
    try:
        success = db.update_onboarding_completion(
            username=current_user,
            onboarding_completed=True,
            tour_completed=request.tour_completed,
            wearable_type=request.wearable_type,
            sleep_goals=request.sleep_goals,
            preferences=request.preferences,
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update onboarding status",
            )

        return {"message": "Onboarding completed successfully"}
    finally:
        db.close()


@router.post("/tour/restart", status_code=status.HTTP_200_OK)
async def restart_tour(current_user: Annotated[str, Depends(get_current_user)]):
    """
    Reset tour completion flag for the current user.

    This allows users to restart the application tour from settings.

    Returns:
        Success message
    """
    db = SleepDatabase()
    try:
        success = db.update_onboarding_completion(
            username=current_user,
            tour_completed=False,
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to restart tour",
            )

        return {"message": "Tour reset successfully"}
    finally:
        db.close()
