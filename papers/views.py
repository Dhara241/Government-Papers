from django.shortcuts import render, Http404
from .utils import get_question_papers
from django.conf import settings
from django.core.paginator import Paginator

def home(request):
    """
    List all exams with optional multi-word smart search and pagination.
    """
    all_papers = get_question_papers()
    query = request.GET.get('q', '').strip().upper()
    
    if query:
        # Normalize common typos for better matching
        normalized_query = query.replace('CLEARK', 'CLERK').replace('CLEARK', 'CLERK')
        query_words = normalized_query.split()
        
        exams = []
        for exam in all_papers.keys():
            exam_upper = exam.upper().replace('CLEARK', 'CLERK')
            
            # Match if ANY of the query words are in the exam name (Broad search)
            # This ensures if they search "GSEB CLEARK", even partial matches like "GSEB" or "CLERK" appear
            if any(word in exam_upper for word in query_words):
                exams.append(exam)
    else:
        exams = list(all_papers.keys())
    
    exams = sorted(exams)
    
    # Pagination
    paginator = Paginator(exams, 10) # 10 entries per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Custom pagination range: Show 1 to 5 and the last page (like in screenshot)
    # Using Django's get_elided_page_range
    custom_page_range = paginator.get_elided_page_range(page_number, on_each_side=2, on_ends=1)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'custom_page_range': custom_page_range,
        'total_entries': len(exams),
        'start_index': page_obj.start_index(),
        'end_index': page_obj.end_index(),
    }
    return render(request, 'papers/home.html', context)

def exam_detail(request, exam_name):
    """
    Show available years for a specific exam.
    """
    all_papers = get_question_papers()
    
    if exam_name not in all_papers:
        raise Http404("Exam not found")
        
    years = all_papers[exam_name].keys()
    
    context = {
        'exam_name': exam_name,
        'years': sorted(years, reverse=True),
    }
    return render(request, 'papers/exam_detail.html', context)

def papers_list(request, exam_name, year):
    """
    List all PDF papers for a specific exam and year.
    """
    all_papers = get_question_papers()
    
    if exam_name not in all_papers or year not in all_papers[exam_name]:
        raise Http404("Papers not found")
        
    papers = all_papers[exam_name][year]
    
    # Handle search/filter within papers
    query = request.GET.get('q', '').strip().lower()
    if query:
        papers = [p for p in papers if query in p.lower()]
        
    context = {
        'exam_name': exam_name,
        'year': year,
        'papers': papers,
        'query': query,
    }
    return render(request, 'papers/papers_list.html', context)
