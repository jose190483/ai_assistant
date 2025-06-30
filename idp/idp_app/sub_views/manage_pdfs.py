import os

from django.shortcuts import render


def manage_pdfs(request):
    import os
    PDF_FOLDER = r"C:\Users\BVM\PycharmProjects\ai_assistant_1\idp\idp_app\pdfs"  # or your actual folder

    message = ''
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith('.pdf')]

    # Handle file upload
    if request.method == 'POST':
        if request.FILES.getlist('pdf_files'):
            uploaded_files = request.FILES.getlist('pdf_files')
            for f in uploaded_files:
                with open(os.path.join(PDF_FOLDER, f.name), 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
            message = f"{len(uploaded_files)} file(s) uploaded successfully."

        # Delete selected PDFs
        elif request.POST.get('delete_selected') == 'true':
            selected_pdfs = request.POST.getlist('selected_pdfs')
            deleted_count = 0
            for file in selected_pdfs:
                file_path = os.path.join(PDF_FOLDER, file)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    deleted_count += 1
            message = f"{deleted_count} selected PDF(s) deleted successfully."

    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith('.pdf')]
    return render(request, 'idp_app/manage_pdfs.html', {
        'message': message,
        'pdf_files': pdf_files
    })
