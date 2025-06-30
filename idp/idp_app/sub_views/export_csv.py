import csv
from django.http import HttpResponse

def export_csv(request):
    keywords = request.session.get('keywords', [])
    found_summary = request.session.get('found_summary', {})

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="search_results.csv"'

    writer = csv.writer(response)
    writer.writerow(['Keyword', 'PDF File', 'Page Number'])

    for kw in found_summary:
        for entry in found_summary[kw]:
            pdf_name, page_num, _ = entry
            writer.writerow([kw, pdf_name, page_num])

    return response
