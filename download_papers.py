import requests
import os

def download_file(url, path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.google.com/'
    }
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=15)
        response.raise_for_status()
        # Check if content type is PDF
        if 'application/pdf' in response.headers.get('Content-Type', ''):
            with open(path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Successfully downloaded: {path}")
            return True
        else:
            print(f"Failed: URL did not return a PDF ({url}). Content-Type: {response.headers.get('Content-Type')}")
            return False
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

# GPSC 2023 - Trying a direct link from a different educational site
papers = [
    {
        'url': 'https://gpsc.gujarat.gov.in/Documents/AdvertismentDocument/RFAK-03-202324.pdf',
        'path': 'media/question_papers/GPSC/2023/Class_1_2_Prelims.pdf'
    },
    {
        'url': 'https://www.tutorialsduniya.com/exams/gpsc-question-papers/', # This is a page, not a direct PDF. Let's try to find a direct PDF.
        'path': 'dummy'
    }
]

# Let's try some other direct links found from previous search
direct_links = [
    ('https://www.tutorialsduniya.com/wp-content/uploads/2023/04/GPSC-Class-1-2-Prelims-Question-Paper-2023-GS-1.pdf', 'media/question_papers/GPSC/2023/Class_1_2_Prelims.pdf'),
    ('https://www.tutorialsduniya.com/wp-content/uploads/2023/04/GPSC-Class-1-2-Prelims-Question-Paper-2023-GS-2.pdf', 'media/question_papers/GPSC/2023/Class_1_2_Mains.pdf'),
    ('https://www.tutorialsduniya.com/wp-content/uploads/2022/04/LRD-Constable-Question-Paper-2022.pdf', 'media/question_papers/Police Bharti/2022/LRD_Constable.pdf')
]

for url, path in direct_links:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    download_file(url, path)
