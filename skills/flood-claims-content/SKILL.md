# FloodClaims Pro — Training Content & Exam Skill

> Complete reference for training modules, lessons, practice exams, and certification testing.

## Architecture Overview

```
/become-agent              → Public landing page
/training                  → Paid class catalog ($50 each)
/training/<slug>           → Class detail + enrollment
/student/dashboard         → Enrolled classes + progress
/student/class/<id>/lesson/<lid>  → Lesson viewer
/practice-exam             → Free practice exam (20 questions)
/practice-exam/results     → Score + review
/apply-adjuster            → Application form
/student/certificate/<eid> → Certificate
```

## Training Content Structure

### Module → Lesson → Content
- **Module**: A training class (e.g., "Flood Damage Fundamentals")
- **Lesson**: Individual lesson within a module (e.g., "Water Categories")
- **Content**: HTML text, video embed, or both

### Content Types
1. **Text Lessons**: HTML content with images, diagrams, charts
2. **Video Lessons**: YouTube/Vimeo embed with transcript
3. **Mixed**: Video + supplementary text + downloadable resources

## Practice Exam System

### Question Pool
- Store questions in database with multiple answers
- Shuffle questions and answers on each attempt
- 20 random questions from pool of 24+
- 80% pass threshold (16/20 correct)

### Question Schema
```sql
CREATE TABLE IF NOT EXISTS exam_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer_a TEXT NOT NULL,
    answer_b TEXT NOT NULL,
    answer_c TEXT NOT NULL,
    answer_d TEXT NOT NULL,
    correct_answer CHAR(1) NOT NULL,  -- A/B/C/D
    explanation TEXT DEFAULT '',
    category TEXT DEFAULT 'general',
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

### Exam Flow
1. Student clicks "Start Practice Exam"
2. System selects 20 random questions from active pool
3. Shuffle answer order (A/B/C/D randomized)
4. Student answers all 20
5. System scores instantly
6. Show: score, pass/fail, correct/incorrect per question, explanations
7. Allow retake after 7 days if failed

### Score Display
```python
score = correct_count / total_questions * 100
passed = score >= 80

if passed:
    message = f"✅ Passed! {correct_count}/{total_questions} ({score:.0f}%)"
else:
    message = f"❌ Not yet. {correct_count}/{total_questions} ({score:.0f}%). Need 80%. Try again in 7 days."
```

## Certification Test

### Requirements
- Must complete all training modules (100% progress)
- Must pass practice exam (80%+)
- Application reviewed by admin

### Certificate Generation
- Unique certificate code: `secrets.token_urlsafe(16)`
- Student name, class title, completion date
- Printable/downloadable format
- Verification URL: `/verify/<code>`

## Seed Content

### Exam Questions (Flood Adjusting)
Sample categories:
- Water Categories (1, 2, 3)
- Damage Classes (1-4)
- NFIP Policy Coverage
- FEMA Guidelines
- Safety Procedures
- Documentation Requirements
- Xactimate Basics
- State Licensing Requirements

### Training Modules (Free on /become-agent)
1. **Flood Damage Fundamentals** (5 lessons)
   - What is flood damage?
   - Water categories explained
   - Damage assessment basics
   - Documentation best practices
   - Safety on the job

2. **Water Categories & Classes** (4 lessons)
   - Category 1: Clean water
   - Category 2: Gray water
   - Category 3: Black water
   - Class 1-4 damage levels

3. **NFIP & FEMA** (5 lessons)
   - NFIP policy basics
   - FEMA flood zone maps
   - Coverage limits
   - Claims process
   - Compliance requirements

4. **Damage Assessment** (4 lessons)
   - Room-by-room assessment
   - Structural damage
   - Contents damage
   - Moisture mapping

5. **Adjuster Licensing** (3 lessons)
   - State licensing requirements
   - Xactimate training
   - Continuing education
   - Career paths

## Key Pitfalls
1. **Always shuffle answers** — store correct_answer but display in random order
2. **Retake cooldown** — 7 days between failed attempts
3. **Progress tracking** — mark lessons complete, update progress bar
4. **Certificate uniqueness** — never reuse certificate codes
5. **Mobile-friendly** — exam must work on phones/tablets
6. **Accessibility** — proper labels, keyboard navigation
