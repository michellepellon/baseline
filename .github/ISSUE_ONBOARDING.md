## Overview

Build a smooth, guided onboarding experience that detects when the application has no data and walks users through initial setup, data upload, configuration, and an interactive tour of the application features.

## User Story

As a new user opening the application for the first time, I want to be guided through setting up my account, connecting my health data, and learning how to use the application, so that I can quickly start tracking and analyzing my sleep patterns.

## Current State

- Application initializes with empty database (no sleep data)
- Default admin user is created automatically
- No detection of "first-run" or "no data" state
- No guided setup process
- Users must discover features on their own

## Proposed Solution

### 1. First-Run Detection

**Backend:**
- Add endpoint `GET /api/onboarding/status` that returns:
  ```json
  {
    "is_onboarded": false,
    "has_sleep_data": false,
    "has_completed_tour": false,
    "wearables_configured": false
  }
  ```
- Check for:
  - Presence of sleep records in database
  - User preferences/settings indicating onboarding completion
  - Profile completeness (name, preferences, etc.)

**Frontend:**
- Check onboarding status on application load
- Redirect to onboarding flow if not completed
- Store onboarding progress in localStorage to support multi-session completion

### 2. Onboarding Workflow Steps

#### Step 1: Welcome & Profile Setup
- Welcome message explaining the application purpose
- Collect user information:
  - First name, last name
  - Optional: profile picture
  - Sleep goals (e.g., "improve sleep quality", "track patterns", "optimize duration")
- Update user profile via existing `/api/auth/profile` endpoint

#### Step 2: Wearables Configuration
- Display supported wearables:
  - ✅ Apple HealthKit (currently supported)
  - 🔜 Other wearables (future: Fitbit, Garmin, Oura, etc.)
- For Apple HealthKit:
  - Instructions on exporting data from iPhone Health app
  - Step-by-step guide with screenshots/illustrations:
    1. Open Health app on iPhone
    2. Tap profile picture (top right)
    3. Scroll to "Export All Health Data"
    4. Wait for export to complete
    5. Save/share the export.zip file
- Mark wearable type in user preferences

#### Step 3: Data Upload
- File upload interface for Apple Health export.zip
- Clear instructions: "Upload your export.zip file from Apple Health"
- Progress indicator during upload and processing
- Use existing `/api/ingest/apple-health` endpoint
- Show import statistics:
  - X sleep records imported
  - Date range: YYYY-MM-DD to YYYY-MM-DD
  - X nights of sleep data
- Handle errors gracefully with clear messaging

#### Step 4: Settings & Preferences
- Sleep preferences:
  - Ideal bedtime range
  - Target sleep duration
  - Time zone
- Notification preferences (if applicable)
- Data visualization preferences:
  - Date format
  - 12hr vs 24hr time
  - Preferred metrics (hours vs minutes)

#### Step 5: Interactive Application Tour
- JavaScript-based guided tour using a library like:
  - [Shepherd.js](https://shepherdjs.dev/) (recommended - accessible, customizable)
  - [Intro.js](https://introjs.com/)
  - [Driver.js](https://driverjs.com/)
- Tour highlights:
  1. **Dashboard Overview**: Main metrics, recent sleep data
  2. **Sleep Insights**: AI-powered health insights
  3. **Trends & Analytics**: Charts and visualizations
  4. **Upload More Data**: How to add new data
  5. **Profile Settings**: Where to manage preferences
  6. **Help & Support**: Where to get help
- Allow users to:
  - Skip tour
  - Restart tour later from settings
  - Navigate forward/backward through steps

### 3. Onboarding Completion

- Mark onboarding as complete in user preferences
- Store completion timestamp
- Add "Restart Tour" option in settings for returning users
- Show success message and redirect to dashboard

## Technical Requirements

### Backend (FastAPI)

**New Endpoints:**
```python
GET  /api/onboarding/status          # Get onboarding status
POST /api/onboarding/complete        # Mark onboarding complete
GET  /api/onboarding/tour/restart    # Reset tour completion flag
```

**Database Schema Changes:**
Add to `users` table:
```sql
ALTER TABLE users ADD COLUMN onboarding_completed BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN onboarding_completed_at TIMESTAMP;
ALTER TABLE users ADD COLUMN tour_completed BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN wearable_type VARCHAR;  -- 'apple_health', 'fitbit', etc.
ALTER TABLE users ADD COLUMN sleep_goals TEXT;       -- JSON array of goals
ALTER TABLE users ADD COLUMN preferences JSON;        -- User preferences
```

### Frontend (Svelte)

**New Components:**
```
src/lib/components/onboarding/
├── OnboardingFlow.svelte          # Main container
├── WelcomeStep.svelte             # Step 1: Welcome & Profile
├── WearablesStep.svelte           # Step 2: Wearables detection
├── DataUploadStep.svelte          # Step 3: Data upload
├── SettingsStep.svelte            # Step 4: Preferences
├── TourStep.svelte                # Step 5: Launch tour
└── ProgressIndicator.svelte       # Progress bar component
```

**Tour Implementation:**
```
src/lib/components/tour/
├── AppTour.svelte                 # Tour configuration & steps
└── tourSteps.ts                   # Tour step definitions
```

**Routing:**
- Add `/onboarding` route
- Protect main routes with onboarding check
- Redirect incomplete users to onboarding flow

### Dependencies to Add

**Frontend:**
```bash
npm install shepherd.js
# or
npm install intro.js
# or
npm install driver.js
```

## Acceptance Criteria

### Must Have
- [ ] Backend detects first-run state (no sleep data)
- [ ] Frontend displays onboarding flow for new users
- [ ] Users can complete profile setup (name, photo)
- [ ] Clear instructions for Apple Health data export
- [ ] File upload works for Apple Health export.zip
- [ ] Progress indicator shows during data processing
- [ ] Success message with import statistics
- [ ] Basic settings configuration (sleep goals, preferences)
- [ ] Interactive tour highlights key features (minimum 5 steps)
- [ ] Tour can be skipped or completed
- [ ] Onboarding completion persists in database
- [ ] Returning users are not shown onboarding again
- [ ] Tour can be restarted from settings

### Should Have
- [ ] Onboarding progress saves between sessions
- [ ] Visual indicators for wearable support status
- [ ] Detailed error messages for failed uploads
- [ ] Preview of imported data before final confirmation
- [ ] Ability to go back to previous onboarding steps
- [ ] Mobile-responsive onboarding UI
- [ ] Tour adapts to mobile/tablet screen sizes
- [ ] Animations/transitions between onboarding steps

### Nice to Have
- [ ] Sample data option to explore app without uploading
- [ ] Video tutorials embedded in onboarding
- [ ] Email confirmation after successful setup
- [ ] Onboarding analytics (track completion rates, drop-off points)
- [ ] A/B test different onboarding flows
- [ ] Contextual help tooltips throughout tour
- [ ] Tour keyboard navigation support

## Implementation Notes

### Tour Library Recommendation: Shepherd.js

**Pros:**
- Highly accessible (ARIA compliant)
- Framework agnostic (works well with Svelte)
- Extensive customization options
- Active maintenance
- Good documentation
- Modal overlays and element highlighting
- Responsive and mobile-friendly

**Example Integration:**
```typescript
import Shepherd from 'shepherd.js';
import 'shepherd.js/dist/css/shepherd.css';

const tour = new Shepherd.Tour({
  useModalOverlay: true,
  defaultStepOptions: {
    classes: 'shepherd-theme-custom',
    scrollTo: true,
    cancelIcon: { enabled: true }
  }
});

tour.addStep({
  id: 'dashboard',
  text: 'This is your sleep dashboard showing your recent sleep patterns.',
  attachTo: { element: '.dashboard-card', on: 'bottom' },
  buttons: [
    { text: 'Skip', action: tour.cancel },
    { text: 'Next', action: tour.next }
  ]
});
```

### Error Handling

- **No data uploaded**: Show helper message, don't block completion
- **Upload fails**: Clear error with retry option and troubleshooting link
- **Partial completion**: Save progress, allow resume
- **Browser refresh**: Restore onboarding state from backend

### Testing Considerations

- [ ] Test with fresh database (no data)
- [ ] Test with existing user (should skip onboarding)
- [ ] Test upload with various Apple Health export files
- [ ] Test tour on different screen sizes
- [ ] Test keyboard navigation for accessibility
- [ ] Test skip/cancel flows
- [ ] Test progress persistence across sessions
- [ ] Test restart tour functionality

### Security Considerations

- Validate file uploads (type, size limits)
- Rate limit onboarding endpoints
- Sanitize user input in profile setup
- Ensure uploaded files are processed in isolated environment

## Related Endpoints

**Existing (to leverage):**
- `POST /api/ingest/apple-health` - Upload Apple Health data
- `PUT /api/auth/profile` - Update user profile
- `GET /api/insights/health` - Get health insights (to showcase in tour)
- `GET /api/sleep/summary` - Get sleep summary (to showcase in tour)

## Success Metrics

- 80%+ of new users complete onboarding
- Average time to complete: < 5 minutes
- 60%+ of users complete the tour
- Reduction in support requests about "how to upload data"
- Increased user retention in first week

## Future Enhancements

- Support for additional wearables (Fitbit, Garmin, Oura Ring, Whoop)
- Direct API integrations (no manual export required)
- Personalized onboarding based on user goals
- Progressive onboarding (spread over multiple sessions)
- Gamification elements (badges, achievements)
- Community features onboarding (if added later)

---

**Priority:** High
**Effort Estimate:** Large (3-5 days)
**Type:** Feature
**Labels:** enhancement, onboarding, UX, frontend, backend
