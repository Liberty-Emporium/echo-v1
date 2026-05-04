#!/bin/bash
cd /root/.openclaw/workspace/echo-v1/course/visuals
for lesson in 1-1 1-2 2-1 2-2 4-1 5-1; do
  echo "===== Capturing $lesson ====="
  python3 capture_lesson.py --lesson $lesson
  echo ""
done
echo "===== ALL DONE ====="
