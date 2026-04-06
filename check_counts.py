import sys
sys.path.insert(0, '.')
from app.routers.bible import CHAPTERS

total = 0
short = []
for ch in CHAPTERS:
    n = len(ch.get('quiz', []))
    total += n
    if n != 10:
        short.append(f"  {ch['id']}: {n} questions")

print(f"Total questions: {total}")
if short:
    print("Chapters with != 10 questions:")
    for s in short:
        print(s)
else:
    print("All chapters have exactly 10 questions.")
