import re

txt_path = r"docs\SmartCity360_OODP_II_Final_Submission-v5.txt"
with open(txt_path, "r", encoding="utf-8") as f:
    content = f.read()

# Backup
with open(r"docs\backup\SmartCity360_OODP_II_Final_Submission-v5.before_slides_insert.txt", "w", encoding="utf-8") as f:
    f.write(content)

replacements = [
    ("📷 [ FIGURE PLACEHOLDER — FIGURE 2.1 ]", 
     "📷 [ FIGURE 2.1 — INSERTED: SmartCity360 Slide 3: Part A, Decorator UML Class Diagram ]"),
    ("📷 [ FIGURE PLACEHOLDER — FIGURE 2.2 ]", 
     "📷 [ FIGURE 2.2 — INSERTED: SmartCity360 Slide 4: Part A, Decorator Runtime Pipeline & Nesting Flowchart ]"),
    ("📷 [ FIGURE PLACEHOLDER — FIGURE 3.1 ]", 
     "📷 [ FIGURE 3.1 — INSERTED: SmartCity360 Slide 5: Part B, Composite UML Class Diagram ]"),
    ("📷 [ FIGURE PLACEHOLDER — FIGURE 3.2 ]", 
     "📷 [ FIGURE 3.2 — INSERTED: SmartCity360 Slide 6: Part B, Composite Zone Tree & Command Broadcast ]"),
    ("📷 [ FIGURE PLACEHOLDER — FIGURE 4.1 ]", 
     "📷 [ FIGURE 4.1 — INSERTED: SmartCity360 Slide 7: Part C, Chain of Responsibility UML Class Diagram ]"),
    ("📷 [ FIGURE PLACEHOLDER — FIGURE 4.2 ]", 
     "📷 [ FIGURE 4.2 — INSERTED: SmartCity360 Slide 8: Part C, Chain of Responsibility Routing Flow ]"),
    ("📷 [ FIGURE PLACEHOLDER — FIGURE 5.1 ]", 
     "📷 [ FIGURE 5.1 — INSERTED: SmartCity360 Slide 9: Part D, Flyweight UML Class Diagram ]"),
    ("📷 [ FIGURE PLACEHOLDER — FIGURE 5.2 ]", 
     "📷 [ FIGURE 5.2 — INSERTED: SmartCity360 Slide 10: Part D, Flyweight Memory Impact at 25,000 Poles ]"),
    ("📷 [ FIGURE PLACEHOLDER — FIGURE 6.1 ]", 
     "📷 [ FIGURE 6.1 — INSERTED: SmartCity360 Slide 11: Part E, Interpreter UML Class Diagram ]"),
    ("📷 [ FIGURE PLACEHOLDER — FIGURE 6.2 ]", 
     "📷 [ FIGURE 6.2 — INSERTED: SmartCity360 Slide 12: Part E, Interpreter AST for Sample Policy ]"),
    ("📷 [ FIGURE PLACEHOLDER — FIGURE 7.1 ]", 
     "📷 [ FIGURE 7.1 — INSERTED: SmartCity360 Slide 1: System Architecture - Four Decoupled Tiers ]"),
    ("📷 [ FIGURE PLACEHOLDER — FIGURE 7.2 ]", 
     "📷 [ FIGURE 7.2 — INSERTED: SmartCity360 Slide 13: System Design - Comprehensive Use Case Diagram ]"),
    ("📷 [ FIGURE PLACEHOLDER — FIGURE 7.3 ]", 
     "📷 [ FIGURE 7.3 — INSERTED: SmartCity360 Slide 14: System Design - Complaint Submission Sequence & Subsystem Interaction ]"),
    ("📷 [ FIGURE PLACEHOLDER — FIGURE 7.4 ]", 
     "📷 [ FIGURE 7.4 — INSERTED: SmartCity360 Slide 15: System Design - Database Model (MySQL 8) ]"),
]

for old, new in replacements:
    count = content.count(old)
    content = content.replace(old, new)
    print(f"Replaced {count} occurrences of {old[:40]}")

with open(txt_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Updated {txt_path} successfully.")

