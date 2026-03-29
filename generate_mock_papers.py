from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_mock_exam_pdf(exam_name, year, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # --- Page 1: Front Page ---
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, height - 100, f"{exam_name} EXAMINATION")
    
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height - 140, f"PREVIOUS YEAR PAPER - {year}")
    
    c.line(50, height - 160, width - 50, height - 160)
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 200, "Time Allowed: 2 Hours")
    c.drawRightString(width - 50, height - 200, "Maximum Marks: 100")
    
    instructions = [
        "INSTRUCTIONS TO CANDIDATES:",
        "1. This paper contains 100 Multiple Choice Questions.",
        "2. All questions carry equal marks.",
        "3. There is a negative marking of 0.33 for each wrong answer.",
        "4. Use only Blue/Black ball point pen for marking answers on the OMR sheet.",
        "5. Please ensure all pages are present in the booklet before starting.",
    ]
    
    y = height - 240
    c.setFont("Helvetica-Bold", 14)
    for line in instructions:
        c.drawString(50, y, line)
        y -= 25
        c.setFont("Helvetica", 12)

    c.drawCentredString(width/2, 50, "Page 1 of 5")
    c.showPage()

    # --- Pages 2-5: Questions ---
    q_num = 1
    for page in range(2, 6):
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, f"Section: General Knowledge & Current Affairs")
        c.line(50, height - 60, width - 50, height - 60)
        
        y = height - 100
        c.setFont("Helvetica", 12)
        
        for _ in range(25): # 25 questions per page
            if q_num > 100: break
            
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, f"Q{q_num}. Sample Question for {exam_name} {year}?")
            y -= 20
            
            c.setFont("Helvetica", 11)
            options = ["(A) Option One", "(B) Option Two", "(C) Option Three", "(D) Option Four"]
            for opt in options:
                c.drawString(70, y, opt)
                y -= 15
            
            y -= 10
            q_num += 1
            
            if y < 100: # New page if needed
                break
        
        c.drawCentredString(width/2, 50, f"Page {page} of 5")
        c.showPage()

    c.save()
    print(f"Generated mock PDF: {filename}")

# Generate for ALL folders found in media/question_papers/
base_path = "media/question_papers"
for exam in os.listdir(base_path):
    exam_path = os.path.join(base_path, exam)
    if os.path.isdir(exam_path):
        for year in os.listdir(exam_path):
            year_path = os.path.join(exam_path, year)
            if os.path.isdir(year_path):
                for file in os.listdir(year_path):
                    if file.endswith(".pdf"):
                        full_path = os.path.join(year_path, file)
                        create_mock_exam_pdf(exam, year, full_path)
