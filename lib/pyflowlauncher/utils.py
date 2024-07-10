from typing import Generator, Iterable
from .result import Result
from .string_matcher import string_matcher, DEFAULT_QUERY_SEARCH_PRECISION as DEFAULT_PRECISION


def score_results(
    query: str,
    results: Iterable[Result],
    score_cutoff: int = DEFAULT_PRECISION,
    match_on_empty_query: bool = False,
) -> Generator[Result, None, None]:
    for result in results:
        match = string_matcher(
            query,
            result.Title,
            query_search_precision=score_cutoff
        )
        if match.matched or (match_on_empty_query and not query):
            result.TitleHighlightData = match.index_list
            result.Score = match.score
            yield result
