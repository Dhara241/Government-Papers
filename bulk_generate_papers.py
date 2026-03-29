import os
import random
from generate_mock_papers import create_mock_exam_pdf

def generate_bulk_papers():
    # Expanded list to represent hundreds of exam types
    exams = []
    prefixes = ["GSSSB", "GPSC", "GPSSB", "GSEB", "AMC", "SMC", "RMC", "VMC", "JMC", "GMC", "GETCO", "DGVCL", "MGVCL", "PGVCL", "UGVCL", "GSRTC", "Police", "High Court", "District Court", "Revenue", "Health", "Education", "Forest", "Agriculture", "Social Welfare", "Tribal Welfare", "Accounts", "Audit", "Statistical", "Engineering", "Technical", "Industrial"]
    
    base_exams = [
        "Clerk", "Senior Clerk", "Head Clerk", "Junior Clerk", "Bin Sachivalay Clerk", "Office Assistant", 
        "Talati Cum Mantri", "Gram Sevak", "Mukhya Sevika", "Nayab Chitnis", "Chitnis", "Mamlatdar", 
        "Section Officer", "State Tax Inspector", "Police Inspector", "Sub Inspector", "Constable", 
        "LRD", "PSI", "ASI", "Driver", "Conductor", "Staff Nurse", "MPHW", "FHW", "Lab Technician", 
        "Pharmacist", "X-Ray Technician", "Assistant Engineer Civil", "Assistant Engineer Electrical", 
        "Assistant Engineer Mechanical", "Junior Engineer", "Vidyut Sahayak", "Accountant", "Auditor", 
        "Sub Auditor", "Statistical Assistant", "Planning Assistant", "Sanitary Inspector", 
        "Forest Guard", "Forester", "Range Forest Officer", "Teacher Class-1", "Teacher Class-2", 
        "TET-1", "TET-2", "TAT Secondary", "TAT Higher Secondary", "Professor", "Lecturer", 
        "Assistant", "Peon", "Watchman", "Driver Class-3", "Technical Assistant", "Cleark"
    ]

    # Generate ~200+ unique exam categories
    for pref in prefixes:
        for base in base_exams:
            if random.random() > 0.6: # Randomly combine to create diversity
                exams.append(f"{pref} {base}")
    
    # Add some specific ones (cleaned names for Windows paths)
    exams.extend([
        "Gujarat Administrative Service Class-1", "Gujarat Civil Service Class-1-2", 
        "DYSO - Nayab Mamlatdar", "State Tax Inspector Class-3", "STI Mains", 
        "GPSC Assistant Professor", "GSSSB CCE Group A", "GSSSB CCE Group B"
    ])
    
    exams = list(set(exams)) # Remove duplicates
    
    years = ["2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015"]
    
    paper_types = ["Prelims", "Mains", "Paper-1", "Paper-2", "GS", "Gujarati", "English", "Maths", "Model Paper", "Final Paper"]
    
    base_path = "media/question_papers"
    os.makedirs(base_path, exist_ok=True)
    
    total_generated = 0
    
    print("Starting bulk generation for hundreds of papers...")
    
    for exam in exams:
        # Each exam will have 3-6 random years from the list
        selected_years = random.sample(years, random.randint(3, 7))
        
        for year in selected_years:
            exam_dir = os.path.join(base_path, exam, year)
            os.makedirs(exam_dir, exist_ok=True)
            
            # Each year will have 1-3 random paper types
            selected_papers = random.sample(paper_types, random.randint(1, 3))
            
            for paper in selected_papers:
                filename = f"{paper.replace(' ', '_')}.pdf"
                full_path = os.path.join(exam_dir, filename)
                
                # Generate a professional multi-page PDF
                create_mock_exam_pdf(exam, year, full_path)
                total_generated += 1
                
                if total_generated % 50 == 0:
                    print(f"Generated {total_generated} papers...")

    print(f"Finished! Total {total_generated} papers generated across {len(exams)} exam categories.")

if __name__ == "__main__":
    generate_bulk_papers()
