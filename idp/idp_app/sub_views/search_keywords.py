import os
import re
import fitz  # PyMuPDF
from collections import defaultdict
from django.shortcuts import render

PDF_FOLDER = r"C:\Users\BVM\PycharmProjects\ai_assistant_1\idp\idp_app\pdfs"

def search_keywords(request):
    highlighted_results = defaultdict(list)
    not_found_keywords = []
    message = ''
    keywords = []

    if request.method == 'POST':
        # ✅ Handle clear PDFs
        if request.POST.get('clear_pdfs') == 'true':
            deleted_count = 0
            for filename in os.listdir(PDF_FOLDER):
                if filename.endswith('.pdf'):
                    os.remove(os.path.join(PDF_FOLDER, filename))
                    deleted_count += 1
            return render(request, 'idp_app/search_page.html', {
                'found_summary': {},
                'not_found_keywords': [],
                'message': f"{deleted_count} PDF(s) deleted successfully.",
                'pdf_files': []
            })

        # ✅ Handle PDF upload
        uploaded_files = request.FILES.getlist('pdf_files')
        if uploaded_files:
            for f in uploaded_files:
                with open(os.path.join(PDF_FOLDER, f.name), 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
            message = f"{len(uploaded_files)} file(s) uploaded successfully."

        # ✅ Handle keyword search
        keywords = request.POST.get('keywords', '')
        keywords = [kw.strip().lower() for kw in keywords.split(',') if kw.strip()]

        if keywords:
            pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith('.pdf')]
            for pdf_name in pdf_files:
                pdf_path = os.path.join(PDF_FOLDER, pdf_name)
                doc = fitz.open(pdf_path)

                for page_num, page in enumerate(doc, start=1):
                    text = page.get_text()
                    text_lower = text.lower()

                    for kw in keywords:
                        if kw in text_lower:
                            # Highlight match
                            pattern = re.compile(re.escape(kw), re.IGNORECASE)
                            highlighted_text = pattern.sub(r'<mark>\g<0></mark>', text)
                            highlighted_results[kw].append(
                                (pdf_name, page_num, highlighted_text)
                            )

            not_found_keywords = [kw for kw in keywords if not highlighted_results[kw]]
    num_pdfs = len([f for f in os.listdir(PDF_FOLDER) if f.endswith('.pdf')])
    num_keywords = len(keywords)
    num_matched = len([kw for kw in highlighted_results if highlighted_results[kw]])
    num_not_found = len(not_found_keywords)
    request.session['keywords'] = keywords
    request.session['found_summary'] = dict(highlighted_results)
    return render(request, 'idp_app/search_page.html', {
        'stats': {
            'pdfs_scanned': num_pdfs,
            'keywords_entered': num_keywords,
            'keywords_matched': num_matched,
            'keywords_not_found': num_not_found,
        },
        'found_summary': dict(highlighted_results),
        'not_found_keywords': not_found_keywords,
        'message': message,
        'pdf_files': [f for f in os.listdir(PDF_FOLDER) if f.endswith('.pdf')]
    })


