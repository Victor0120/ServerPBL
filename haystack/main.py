from haystack import Finder
from haystack.preprocessor.cleaning import clean_wiki_text
from haystack.preprocessor.utils import convert_files_to_dicts, fetch_archive_from_http
from haystack.reader.farm import FARMReader
from haystack.reader.transformers import TransformersReader
from haystack.utils import print_answers
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.retriever.sparse import ElasticsearchRetriever
from importlib import reload
import sys
from multiprocessing import freeze_support


def main():
    # Data path
    doc_dir = "..\\..\\data\\rc"

    document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")


    # DocumentStore: holds all your data
    document_store = ElasticsearchDocumentStore()

    # Clean & load your documents into the DocumentStore
    # dicts = convert_files_to_dicts(doc_dir, clean_func=clean_wiki_text)
    dicts = convert_files_to_dicts(dir_path=doc_dir, clean_func=clean_wiki_text, split_paragraphs=True)
    document_store.write_documents(dicts)

    # Retriever: A Fast and simple algo to indentify the most promising candidate documents
    retriever = ElasticsearchRetriever(document_store)

    # Reader: Powerful but slower neural network trained for QA
    model_name = "deepset/roberta-base-squad2"
    reader = FARMReader(model_name, use_gpu=False)

    # Finder: Combines Reader and Retriever
    finder = Finder(reader, retriever)

    while (True):
        question = input("User: ")
        prediction = finder.get_answers(question)
        print_answers(prediction)
        print()

if __name__ == '__main__':
    freeze_support()
    main()