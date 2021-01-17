import requests

from flask import current_app
from models import Course
import time
import fitz
import uuid
import os

def get_answers(question, course_id, n_top):
    # for testing wihtout model connection
    time.sleep(3)
    sample_answers =  [
        {
            'message': 'sample answer1'
        },
        {
            'message': 'sample answer2 long Lorem Ipsum has been the industry"s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting'
        },
        {
            'message': 'message with document',
            'doc_path': 'http://localhost:5000/static/course/temp/1/6.1-TheDataLinkLayer.pdf'
        }
    ]
    #return sample_answers
    # end testing block #

    course = Course.query.get(course_id)
    doc_model_id = course.doc_model_id
    faq_model_id = course.doc_model_id

    doc_url = current_app.config['QA_API_BASE_URL'] + f'models/doc-qa/questions' 
    faq_url = current_app.config['QA_API_BASE_URL'] + f'models/faq-qa/questions'

    json_data = {
        "questions": [question],
        "top_k_reader": n_top,
    }

    answers = []
    
    if faq_url:
        json_data['model_id'] = faq_model_id
        r = requests.post(url=faq_url, json=json_data).json()

        if len(r[0]['answers']):
            top_answer = r[0]['answers'][0]
            
            if top_answer['probability'] > 80:
                answers.append({
                    'message': top_answer['answer']
                })
                
                return answers

    if doc_url:
        json_data['model_id'] = doc_model_id
        r = requests.post(url=doc_url, json=json_data).json()
        answers.extend([answer for answer in r[0]['answers'] if answer['probability'] > 0.54])
        
    sorted_answers = sorted(answers, key=lambda k: k['probability'])
    clean_answers = []

    for i in range(min(n_top, len(sorted_answers))):
        answer_text = sorted_answers[i]['answer']
        answer_context = sorted_answers[i]['context']
        filename = sorted_answers[i]['meta'].get('name', '') # or link for faq
        file_loc = highlight_pdf(course_id, filename, answer_context, answer_text)

        answer = {
            'message': answer_text,
            'doc_path': current_app.config['BASE_URL'] + '/' + file_loc
        }

        clean_answers.append(answer)

    print(clean_answers)

    return clean_answers


def highlight_pdf(course_id, filename, context, answer):
    dir_loc = os.path.join('static', 'course', 'materials', str(course_id))
    file_loc = os.path.join(dir_loc, filename)
    doc = fitz.open(file_loc)

    highlight_count = 0
    highlight_page  = 1

    for i, page in enumerate(doc, 1):
        y_min = 100000
        y_max = 0

        for inst in page.searchFor(context):
            y_min = min(y_min, inst.y0)
            y_max = max(y_max, inst.y1)

            highlight = page.addHighlightAnnot(inst)
            highlight.setColors({"stroke": (1, 1, 0.91), "fill": (0.75, 0.8, 0.95)})
            highlight.update()


        for inst in page.searchFor(answer):
            # skip if answer rectangle outside context
            if inst.y0 > y_max or inst.y0 < y_min or inst.y1 > y_max or inst.y0 < y_min:
                continue

            highlight = page.addHighlightAnnot(inst)
            highlight_page = i
            highlight_count += 1

    if highlight_count == 0:
        for page in doc:
            for inst in page.searchFor(answer):
                highlight = page.addHighlightAnnot(inst)

    out_dir_loc = os.path.join('static', 'course', 'temp_files', str(course_id))
    out_file_loc = os.path.join(out_dir_loc, str(uuid.uuid4()) + filename)

    if not os.path.exists(out_dir_loc):
        os.makedirs(out_dir_loc)

    doc.save(out_file_loc, garbage=4, deflate=True, clean=True)

    return out_file_loc + f"#page={highlight_page}"

    

def upload_file(course_id, file_loc):
    course = Course.query.get(course_id)
    model_id = course.doc_model_id

    with open(file_loc, 'rb') as f:
        files = {'file': f}
        data =  {'model_id': model_id}
        url = 'http://localhost:8000/models/doc-qa/'
        
        r = requests.post(url, files=files, data=data)
        r.raise_for_status()


def delete_file_from_api(filename, course_id):
    course = Course.query.get(course_id)
    model_id = course.doc_model_id

    url = current_app.config['QA_API_BASE_URL'] + 'models/doc-qa'
    r = requests.delete(url, params={'model_id': model_id, 'filename': filename})
    r.raise_for_status()


def delete_question_answer_from_api(question, answer, course_id):
    course = Course.query.get(course_id)
    model_id = course.faq_model_id

    url = current_app.config['QA_API_BASE_URL'] + 'models/faq-qa'
    r = requests.delete(url, params={'model_id': model_id, 'question': question, 'answer': answer})
    r.raise_for_status()