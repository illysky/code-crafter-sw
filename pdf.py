from PyPDF2 import PdfReader

def extract_text_between_sentences(pdf_path, start_sentence, end_sentence):
    text = ""
    start_index = None
    end_index = None
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            page_text = page.extract_text()
            start_index = page_text.find(start_sentence)
            if start_index != -1:
                text += page_text[start_index:]
                break
        for page_num in range(page_num + 1, num_pages):
            page = reader.pages[page_num]
            page_text = page.extract_text()
            end_index = page_text.find(end_sentence)
            if end_index != -1:
                text += page_text[:end_index + len(end_sentence)]
                break
            else:
                text += page_text
    return text

# Example usage
pdf_path = "awinic.pdf"  # Replace with your PDF file path
start_sentence = "Register Detailed Description"
end_sentence = "Application Information"
extracted_text = extract_text_between_sentences(pdf_path, start_sentence, end_sentence)
print(extracted_text)

with open("output1.txt", "w") as output:
    output.write(extracted_text)
