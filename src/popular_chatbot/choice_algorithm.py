from src.common_utils.language_utils.statement_utils import complex_intersection


def find_max_coverage(documents, tags):
    max_coverage = 0
    for doc in documents:
        tags_from_document = doc['tags']
        coverage = complex_intersection(set(tags_from_document), set(tags), True)
        max_coverage = max(max_coverage, coverage)
    return max_coverage


def find_best_tags_response(documents, tags):
    max_confidence = 0
    max_id = None
    max_cov = find_max_coverage(documents, tags)
    if max_cov == 0:
        return None, None
    is_single_tag = (len(tags) == 1)
    for doc in documents:
        tags_from_document = doc['tags']
        if not is_single_tag and len(tags_from_document) == 1:
            continue
        coverage = complex_intersection(set(tags_from_document), set(tags), True)
        if coverage == max_cov:
            tags_len_diff = len(tags) - coverage if len(tags) > coverage else 0
            conf = (coverage / len(tags_from_document)) - (tags_len_diff * 0.1)
            if conf > max_confidence:
                max_confidence = conf
                max_id = doc['_id']

    result = list(filter(lambda doc: doc['_id'] == max_id, documents))
    if len(result) > 0:
        return result[0]['text'], max_confidence
    else:
        return None, None
