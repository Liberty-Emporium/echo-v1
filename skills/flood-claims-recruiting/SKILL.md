# FloodClaims Pro — Recruiting & Team Management Skill

> Complete reference for the recruit pipeline, invitation system, team roles, and adjuster onboarding.

## Architecture Overview

```
/admin/recruit                    → Recruit dashboard (email settings + invite)
/admin/recruit/send-invite        → Send invitation email
/admin/recruit/adjuster/<id>/approve  → Approve adjuster application
/admin/recruit/contractor/<id>    → Contractor detail + training progress
/admin/team                       → Full team management
/admin/team/<id>/edit             → Edit user
/admin/team/<id>/deactivate       → Deactivate user
/admin/team/<id>/reactivate       → Reactivate user
```

## User Roles (Tiered Access)

| Role | Dashboard | Claims | Team | Recruit | Training | Settings | Analytics |
|------|-----------|--------|------|---------|----------|----------|-----------|
| Admin | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Manager | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Adjuster | ✅ | ✅ own | ❌ | ❌ | ❌ | ❌ | ❌ |

## Team Management Routes

### Create User (Admin)
```python
db.execute(
    'INSERT INTO users (email, name, password, role, is_active) VALUES (?,?,?,?,?)',
    (email, name, hash_pw(password), role, 1)
)
```

### Deactivate User
```python
# Prevent deactivating last admin
admin_count = db.execute("SELECT COUNT(*) FROM users WHERE role='admin' AND is_active=1").fetchone()[0]
if admin_count <= 1 and user['role'] == 'admin':
    flash('Cannot deactivate the last admin.', 'error')
else:
    db.execute('UPDATE users SET is_active=0 WHERE id=?', (user_id,))
```

### Login Check (is_active)
```python
if not user.get('is_active', 1):
    flash('Your account has been deactivated. Contact your administrator.', 'error')
    return render_template('login.html')
```

## Recruitment Pipeline

### 1. Email Settings
- Store `from_email` in settings table
- Verify SendGrid API key is configured
- Show status indicator (✅ configured / ⚠️ not configured)

### 2. Send Invitation
```python
send_email(
    to_email=invite_email,
    subject="🌊 You're Invited — Join FloodClaims Pro",
    html_body=render_template('emails/recruit_invite.html', 
                              name=invite_name, join_url=join_url)
)
```

### 3. Application Types
- **Licensed Adjuster**: Verify license → auto-approve or manual review
- **Contractor → Adjuster**: Training modules → certification test → activate

### 4. Contractor Training Pipeline
1. Apply with contractor license
2. Admin approves for training
3. Complete training modules
4. Pass certification test (80%+)
5. Admin certifies → role becomes 'adjuster'

## Email Templates

### Recruitment Invite
- Professional HTML email with FloodClaims Pro branding
- "Get Started — It's Free" CTA button
- Link to /become-agent public page
- Unsubscribe footer

### Application Received (Admin Notification)
- New application details
- Review/Approve link

### Application Approved (Applicant Notification)
- Welcome message
- Login credentials (temp password)
- Link to dashboard

## Database Schema Additions

### Training Modules (contractor onboarding)
```sql
CREATE TABLE IF NOT EXISTS training_modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT DEFAULT '',
    sort_order INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

### Seed Training Modules
1. Flood Damage Fundamentals
2. Water Categories & Classification
3. NFIP & FEMA Guidelines
4. Damage Assessment Techniques
5. Adjuster Licensing Requirements

## Key Pitfalls
1. **Never allow last admin to be deactivated** — always check count first
2. **Inactive users cannot log in** — check is_active at login AND on every admin action
3. **Manager ≠ Admin** — managers can't access settings or see all analytics
4. **Email validation** — always validate email format before sending
5. **CSRF on all POST routes** — @csrf_required decorator
6. **Temp passwords** — use secrets.token_urlsafe(10) for new accounts
