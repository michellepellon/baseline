"""
Authentication endpoints.
"""

import base64
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from backend.auth.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    verify_token,
)
from backend.auth.users import authenticate_user, get_user, update_user_profile

router = APIRouter(prefix="/api/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


class Token(BaseModel):
    """Token response model."""

    access_token: str
    token_type: str


class UserResponse(BaseModel):
    """User response model."""

    username: str
    first_name: str | None = None
    last_name: str | None = None
    profile_picture_url: str | None = None


class UpdateProfileRequest(BaseModel):
    """Update profile request model."""

    first_name: str | None = None
    last_name: str | None = None


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    """Get the current authenticated user from token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = get_user(username)
    if user is None:
        raise credentials_exception

    return username


@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Login endpoint using OAuth2 password flow.

    Returns:
        JWT access token
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: Annotated[str, Depends(get_current_user)]):
    """
    Get current user information.

    Returns:
        Current user details
    """
    user = get_user(current_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    profile_picture_url = None
    if user.profile_picture:
        profile_picture_url = "/api/auth/profile-picture"

    return {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "profile_picture_url": profile_picture_url,
    }


@router.put("/me", response_model=UserResponse)
async def update_me(
    profile: UpdateProfileRequest,
    current_user: Annotated[str, Depends(get_current_user)],
):
    """
    Update current user profile.

    Returns:
        Updated user details
    """
    user = update_user_profile(
        current_user, first_name=profile.first_name, last_name=profile.last_name
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    profile_picture_url = None
    if user.profile_picture:
        profile_picture_url = "/api/auth/profile-picture"

    return {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "profile_picture_url": profile_picture_url,
    }


@router.post("/profile-picture")
async def upload_profile_picture(
    file: UploadFile,
    current_user: Annotated[str, Depends(get_current_user)],
):
    """
    Upload a profile picture.

    Returns:
        Success message
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_types)}",
        )

    # Validate file size (5MB max)
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds 5MB limit",
        )

    # Update user profile with picture
    user = update_user_profile(
        current_user,
        profile_picture=contents,
        profile_picture_mime_type=file.content_type,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return {"message": "Profile picture uploaded successfully"}


@router.get("/profile-picture")
async def get_profile_picture(
    current_user: Annotated[str, Depends(get_current_user)],
):
    """
    Get the current user's profile picture.

    Returns:
        Profile picture image
    """
    user = get_user(current_user)
    if not user or not user.profile_picture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile picture not found"
        )

    return Response(
        content=bytes(user.profile_picture),
        media_type=user.profile_picture_mime_type or "image/jpeg",
    )


@router.delete("/profile-picture")
async def delete_profile_picture(
    current_user: Annotated[str, Depends(get_current_user)],
):
    """
    Delete the current user's profile picture.

    Returns:
        Success message
    """
    user = update_user_profile(
        current_user, profile_picture=b"", profile_picture_mime_type=None
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return {"message": "Profile picture deleted successfully"}
