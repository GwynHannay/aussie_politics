import utils.legislation_crawler as crawler
import utils.diff_builder as diff


document_filepath = 'docs'

def main():
    constitution_id = crawler.get_constitution()
    constitution_metadata = crawler.get_series(constitution_id)
    updated_metadata = []
    document_order = {}

    for document in constitution_metadata:
        download_page_metadata = crawler.get_download_details(document)
    #     completed_metadata = crawler.download_file(download_page_metadata, document_filepath)
    #     updated_metadata.append(completed_metadata)
    #     document_order[document['Comp No.']] = completed_metadata

    # previous_document = ''
    # for document in sorted(document_order):
    #     if document == '0':
    #         previous_document = document
    #         continue

    #     diff.generate_diff_page(document_order[previous_document], document_order[document], document_filepath)
    #     previous_document = document


if __name__ == "__main__":
    main()