import os
import pdfplumber
from question.models import Subject, Question, Option

BASE_STORAGE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'storage')

def extract_questions_from_pdf(pdf_path):
    """
    Extracts questions and options from a PDF.
    Assumes:
    - Questions are numbered: 1. Question text
    - Options start with a, b, c, d
    - Correct option is marked with (*) e.g., a) Option1 (*)
    """
    questions_list = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            current_question = None
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    # Detect question (numbered)
                    if line[0].isdigit() and line[1] == '.':
                        if current_question:
                            questions_list.append(current_question)
                        current_question = {'text': line, 'options': []}
                    # Detect options (a), b), etc.)
                    elif line[0].lower() in ['a','b','c','d'] and line[1] in [')','.']:
                        is_correct = '(*' in line or '(*)' in line
                        option_text = line.replace('(*)','').replace('(*','').strip()
                        if current_question:
                            current_question['options'].append({'text': option_text, 'is_correct': is_correct})
            # Add last question
            if current_question:
                questions_list.append(current_question)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return questions_list

def process_all_pdfs():
    """Process all PDFs in storage and save questions to DB"""
    for grade_folder in os.listdir(BASE_STORAGE):
        grade_path = os.path.join(BASE_STORAGE, grade_folder)
        if not os.path.isdir(grade_path):
            continue
        grade_number = grade_folder.replace('grade','')
        for subject_folder in os.listdir(grade_path):
            subject_path = os.path.join(grade_path, subject_folder)
            if not os.path.isdir(subject_path):
                continue
            # Create or get Subject
            subject_obj, _ = Subject.objects.get_or_create(name=subject_folder.capitalize())
            for pdf_file in os.listdir(subject_path):
                if not pdf_file.endswith('.pdf'):
                    continue
                pdf_path = os.path.join(subject_path, pdf_file)
                questions = extract_questions_from_pdf(pdf_path)
                for q in questions:
                    question_obj = Question.objects.create(
                        subject=subject_obj,
                        grade=grade_number,
                        text=q['text'],
                        status='published'
                    )
                    for opt in q['options']:
                        Option.objects.create(
                            question=question_obj,
                            text=opt['text'],
                            is_correct=opt['is_correct']
                        )
                print(f"Processed {pdf_file} ({len(questions)} questions)")

if __name__ == "__main__":
    process_all_pdfs()
