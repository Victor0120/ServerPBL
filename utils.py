import requests

from flask import current_app
from models import Course
import time

def get_answers(question, course_id, n_top):
    # for testing wihtout model connection
    time.sleep(3)
    sample_answers =  [
        {
            'message': 'sample answer1'
        },
        {
            'message': 'sample answer2 long Lorem Ipsum has been the industry"s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting'
        }
    ]
    print(sample_answers)
    return sample_answers
    # end testing block #

    course = Course.query.get(course_id)
   # doc_model = course.faq_model_id
   # faq_model = course.doc_model_id
    faq_model_id = 'faq_qa497842236550'
    doc_model_id = 'doc_qa245864938385'

    doc_url = current_app.config['QA_API_BASE_URL'] + f'models/doc-qa/{doc_model_id}/questions' 
    faq_url = current_app.config['QA_API_BASE_URL'] + f'models/faq-qa/{faq_model_id}/questions'

    json_data = {
        "questions": [question],
        "top_k_reader": n_top
    }

    answers = []
    
    if faq_url:
        r = requests.post(url=faq_url, json=json_data).json()
        answers.extend([answer for answer in r[0]['answers'] if answer['probability'] > 80])
    
    if doc_url:
        r = requests.post(url=doc_url, json=json_data).json()
        answers.extend([answer for answer in r[0]['answers'] if answer['probability'] > 0.5])
        
    sorted_answers = sorted(answers, key=lambda k: k['probability'])
    clean_answers = []

    for i in range(min(n_top, len(sorted_answers))):
        answer_text = sorted_answers[i]['answer']
        answer_link = sorted_answers[i]['meta'].get('name', '') # or link for faq

        answer = {
            'message': answer_text
        }

        clean_answers.append(answer)

    print(clean_answers)

    return clean_answers


def upload_file(course_id, file_loc):
    model_id = 'doc_qa245864938385'

    files = {'file': open(file_loc, 'rb')}
    data =  {'model_id': model_id}
    url = current_app.config['MODEL_ENDPOINT'] + 'models/doc-qa'
    
    r.requests.post(url, files=files)
    return r.status_code == 200


def delete_file_from_api(filename, course_id):
    course = Course.query.get(course_id)
    model_id = course.faq_model_id

    url = current_app.config['MODEL_ENDPOINT'] + 'models/doc-qa'
    r = requests.delete(url, json={'model_id': model_id, 'filename': filename})

    return r.status_code == 200


def delete_question_answer(question, answer, course_id):
    course = Course.query.get(course_id)
    model_id = course.doc_model_id

    url = current_app.config['MODEL_ENDPOINT'] + 'models/faq-qa'
    r = requests.delete(url, json={'model_id': model_id, 'question': question, 'answer': answer})

    return r.status_code == 200
