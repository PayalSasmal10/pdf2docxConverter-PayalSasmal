from docx import Document
from pdfconverter.settings import BASE_DIR
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from djangoconvertvdoctopdf.convertor import StreamingConvertedPdf
from pdf2docx import Converter
import os, fnmatch, mimetypes
from django.conf import settings
from django.http.response import HttpResponse



# Create your views here.
def uploadfile(request):
    if request.method == "POST":
        if 'pdf' in request.POST:
            uploaded_file = request.FILES['document']
            convFile = StreamingConvertedPdf(uploaded_file)
            return convFile.stream_content()
        else:
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            fs.save(uploaded_file.name, uploaded_file)
            listOfFiles = os.listdir('./media')
            pattern = "*.pdf"
            for entry in listOfFiles:
                if fnmatch.fnmatch(entry, pattern):
                        pdfPath = os.path.join(BASE_DIR, 'media', entry)
                        cv = Converter(pdfPath)      
                        removeExtension = os.path.splitext(pdfPath)[0]
                        doc = Document()
                        doc.save(removeExtension + '.docx')
                        docPath = os.path.join(BASE_DIR, 'media', removeExtension + '.docx')
                        cv.convert(docPath)
                        cv.close()
                        readFile = open(docPath, 'rb')
                        mime_type, _ = mimetypes.guess_type(docPath)
                        response = HttpResponse(readFile, content_type=mime_type)
                        filename = os.path.basename(docPath)
                        print(filename)
                        response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
                        fs.delete(uploaded_file.name)
                        fs.delete(readFile.name)
                        return response 

    return render(request, 'upload.html')

