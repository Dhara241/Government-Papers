import os
from django.conf import settings
from django.core.cache import cache

def get_question_papers():
    """
    Scans media/question_papers/ and returns a dictionary structure.
    Structure: { 'ExamName': { 'Year': ['file1.pdf', 'file2.pdf'] } }
    """
    cache_key = 'question_papers_structure'
    data = cache.get(cache_key)
    
    if data is not None:
        return data

    base_path = os.path.join(settings.MEDIA_ROOT, 'question_papers')
    papers_data = {}

    if not os.path.exists(base_path):
        return {}

    try:
        # List all exam folders (GPSC, GSSSB, etc.)
        exams = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        
        for exam in exams:
            exam_path = os.path.join(base_path, exam)
            papers_data[exam] = {}
            
            # List all year folders within each exam
            years = [d for d in os.listdir(exam_path) if os.path.isdir(os.path.join(exam_path, d))]
            
            for year in years:
                year_path = os.path.join(exam_path, year)
                # List all PDF files within each year
                files = [f for f in os.listdir(year_path) if os.path.isfile(os.path.join(year_path, f)) and f.endswith('.pdf')]
                
                if files:
                    papers_data[exam][year] = sorted(files)
            
            # Remove exam if no years/files found
            if not papers_data[exam]:
                del papers_data[exam]
                
    except Exception as e:
        print(f"Error scanning directory: {e}")
        return {}

    # Cache the result for 15 minutes
    cache.set(cache_key, papers_data, 900)
    return papers_data
