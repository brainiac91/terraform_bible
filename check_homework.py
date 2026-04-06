import sys
sys.path.insert(0, '.')
from app.routers.bible import CHAPTERS

missing = [c['id'] for c in CHAPTERS if 'homework' not in c]
if missing:
    print(f'Missing homework: {missing}')
else:
    print(f'All {len(CHAPTERS)} chapters have homework assignments.')

for c in CHAPTERS:
    hw = c.get('homework', {})
    title = hw.get('title', 'MISSING')
    diff = hw.get('difficulty', '?')
    steps = len(hw.get('steps', []))
    print(f"  {c['id']}: {title} [{diff}] - {steps} steps")
