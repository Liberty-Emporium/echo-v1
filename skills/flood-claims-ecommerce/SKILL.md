# FloodClaims Pro — E-Commerce & Training System Skill

> Complete reference for the paid training class system, Stripe integration, enrollment flow, and certificate generation.

## Architecture Overview

```
/training              → Public catalog (all published classes)
/training/<slug>       → Class detail + Enroll button ($50)
/training/<slug>/enroll  → Stripe checkout → /training/success
/student/dashboard     → My enrolled classes, progress, certificates
/student/class/<id>/lesson/<lid>  → View lesson (enrolled only)
/student/class/<id>/lesson/<lid>/complete  → AJAX mark complete
/student/certificate/<eid>  → Certificate display/print
/admin/training        → Manage classes, view enrollments
/admin/training/save   → Create/edit class
/admin/training/<id>/enrollments  → View students
```

## Database Schema

### training_classes
| Field | Type | Notes |
|-------|------|-------|
| id | INTEGER PK | |
| title | TEXT | Class name |
| slug | TEXT UNIQUE | URL-friendly |
| description | TEXT | Full HTML description |
| price_cents | INTEGER | Default 5000 ($50.00) |
| duration_hours | INTEGER | Estimated hours |
| level | TEXT | beginner/intermediate/advanced |
| icon | TEXT | Emoji icon |
| syllabus | TEXT | JSON array of lesson titles |
| is_published | INTEGER | 0=draft, 1=published |
| is_featured | INTEGER | Featured on homepage |
| students_count | INTEGER | Denormalized count |
| rating | REAL | Average rating |
| created_at | TEXT | |
| updated_at | TEXT | |

### class_lessons
| Field | Type | Notes |
|-------|------|-------|
| id | INTEGER PK | |
| class_id | INTEGER FK | → training_classes.id |
| title | TEXT | Lesson name |
| content | TEXT | HTML content |
| video_url | TEXT | YouTube/embed URL |
| sort_order | INTEGER | Display order |
| duration_minutes | INTEGER | Estimated minutes |
| is_free_preview | INTEGER | 0=no, 1=yes |

### class_enrollments
| Field | Type | Notes |
|-------|------|-------|
| id | INTEGER PK | |
| user_id | INTEGER FK | → users.id |
| class_id | INTEGER FK | → training_classes.id |
| stripe_session_id | TEXT | Stripe checkout session |
| payment_status | TEXT | pending/paid/refunded |
| progress | INTEGER | 0-100 percentage |
| completed_lessons | TEXT | JSON array of lesson IDs |
| started_at | TEXT | Enrollment date |
| completed_at | TEXT | Completion date |
| certificate_issued | INTEGER | 0/1 |
| certificate_code | TEXT | Unique verify code |

## Stripe Integration

### One-Time Payment Checkout ($50)
```python
import stripe as _stripe

_stripe.api_key = get_setting('stripe_secret_key') or os.environ.get('STRIPE_SECRET_KEY', '')

session = _stripe.checkout.Session.create(
    mode='payment',
    customer_email=user_email,
    line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {'name': class_title},
            'unit_amount': 5000,  # $50.00
        },
        'quantity': 1,
    }],
    success_url=url_for('training_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
    cancel_url=url_for('training_class', slug=slug, _external=True),
    metadata={'class_id': str(class_id), 'user_id': str(user_id)},
)
return redirect(session.url)
```

### Success Handler
```python
@app.route('/training/success')
def training_success():
    session_id = request.args.get('session_id')
    if session_id:
        cs = _stripe.checkout.Session.retrieve(session_id)
        if cs.payment_status == 'paid':
            # Create or update enrollment
            enrollment = get_or_create_enrollment(cs.metadata)
            enrollment.payment_status = 'paid'
            enrollment.stripe_session_id = session_id
            db.commit()
            flash('Payment successful! You now have access to the class.', 'success')
            return redirect(url_for('student_dashboard'))
    flash('Payment verification failed.', 'error')
    return redirect(url_for('training_catalog'))
```

## Certificate Generation

### Certificate Code
```python
import secrets
cert_code = secrets.token_urlsafe(16)  # e.g., "aBcDeFgHiJkLmNoP"
```

### Certificate Template Data
- Student name (from users.name)
- Class title (from training_classes.title)
- Completion date (from class_enrollments.completed_at)
- Certificate code (unique, verifiable)
- FloodClaims Pro branding

### Issue Certificate (when progress = 100%)
```python
if progress >= 100 and not enrollment.certificate_issued:
    enrollment.certificate_issued = 1
    enrollment.certificate_code = secrets.token_urlsafe(16)
    enrollment.completed_at = datetime.utcnow().isoformat()
    db.commit()
```

## Permission Checks

### View Lesson (must be enrolled + paid)
```python
enrollment = db.execute(
    'SELECT * FROM class_enrollments WHERE user_id=? AND class_id=?',
    (session['user_id'], class_id)
).fetchone()

if not enrollment or enrollment['payment_status'] != 'paid':
    flash('You must purchase this class to access lessons.', 'error')
    return redirect(url_for('training_class', slug=slug))
```

### Mark Lesson Complete
```python
# Get current completed lessons
completed = json.loads(enrollment['completed_lessons'] or '[]')
if lesson_id not in completed:
    completed.append(lesson_id)
    
    # Calculate progress
    total_lessons = db.execute('SELECT COUNT(*) FROM class_lessons WHERE class_id=?', (class_id,)).fetchone()[0]
    progress = int(len(completed) / total_lessons * 100)
    
    db.execute('UPDATE class_enrollments SET completed_lessons=?, progress=? WHERE id=?',
               (json.dumps(completed), progress, enrollment['id']))
```

## URL Routes Summary

| URL | Method | Auth | Description |
|-----|--------|------|-------------|
| /training | GET | Public | Class catalog |
| /training/<slug> | GET | Public | Class detail |
| /training/<slug>/enroll | POST | Login | Stripe checkout |
| /training/success | GET | Login | Payment success |
| /student/dashboard | GET | Login | My classes |
| /student/class/<id>/lesson/<lid> | GET | Enrolled | View lesson |
| /student/class/<id>/lesson/<lid>/complete | POST | Enrolled | Mark complete |
| /student/certificate/<eid> | GET | Login | View certificate |
| /admin/training | GET | Admin | Manage classes |
| /admin/training/save | POST | Admin | Save class |
| /admin/training/<id>/enrollments | GET | Admin | View students |

## Key Pitfalls
1. **Always verify payment_status = 'paid'** before granting lesson access
2. **Use cents (5000) not dollars (50)** for Stripe API
3. **Certificate codes must be unique** — use secrets.token_urlsafe(16)
4. **Progress calculation**: len(completed_lessons) / total_lessons * 100
5. **CSRF protection** on all POST routes with @csrf_required
6. **Denormalized students_count** — update on enrollment, not on every page load
