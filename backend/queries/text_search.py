"""
Search text -> safe full-text queries, and ranking of name matches.

Search text is never written into Cypher: it is cleaned into words here and
passed to the database as a query parameter.
"""
import re

LUCENE_RESERVED_PATTERN = re.compile(r'[+\-!(){}\[\]^"~*?:\\/|&]+')
LUCENE_BOOLEAN_OPERATORS = {"AND", "OR", "NOT"}

# Characters that split both search text and names into words: Lucene's
# syntax characters plus common name punctuation. Apostrophes stay inside
# words, as they do in the full-text index (O'Brien).
WORD_SEPARATORS = '+-!(){}[]^"~*?:\\/|&.,;_'
_SEPARATOR_PATTERN = re.compile("[\\s" + re.escape(WORD_SEPARATORS) + "]+")


def tokenize(text: str | None) -> list[str]:
    """Lower-cased words of `text`, without Lucene syntax or operators.
    Apostrophes are kept inside words only (O'Brien, not Rivera')."""
    words = (
        word.strip("'").lower()
        for word in _SEPARATOR_PATTERN.split(text or ""))
    return [
        word for word in words
        if word and word.upper() not in LUCENE_BOOLEAN_OPERATORS
    ]


def build_prefix_query(text: str | None) -> str:
    """A full-text query matching any of the words, each as the start of a
    word: "Ant Riv" -> "ant* riv*". Partial matches are ranked separately."""
    words = tokenize(text)
    if not words:
        raise ValueError("Query parameter is required")
    return " ".join(f"{word}*" for word in words)


def build_all_words_query(text: str | None) -> str:
    """A full-text query requiring every word: "John Doe" -> "+john +doe"."""
    words = tokenize(text)
    if not words:
        raise ValueError("Query parameter is required")
    return " ".join(f"+{word}" for word in words)


def escape_lucene(text: str) -> str:
    """`text` with Lucene syntax characters escaped."""
    return LUCENE_RESERVED_PATTERN.sub(
        lambda m: "".join("\\" + c for c in m.group()), text)


def build_exact_query(text: str | None) -> str:
    """A full-text query for text kept as written (ranks, badge numbers):
    Lucene syntax escaped and stray boolean operators dropped."""
    words = [
        escape_lucene(word) for word in (text or "").split()
        if word.upper() not in LUCENE_BOOLEAN_OPERATORS
    ]
    if not words:
        raise ValueError("Query parameter is required")
    return " ".join(words)


_CYPHER_SEPARATORS = "[" + ", ".join(
    "'" + c.replace("\\", "\\\\") + "'" for c in WORD_SEPARATORS) + "]"


def _words_cypher(expr: str) -> str:
    """Cypher for the lower-cased words of a name, split like tokenize()."""
    return (
        "[part IN split(reduce(text = toLower(coalesce("
        f"{expr}, '')), sep IN {_CYPHER_SEPARATORS} | "
        "replace(text, sep, ' ')), ' ') WHERE part <> '']"
    )


NAME_RANK_ORDER = (
    "name_tier ASC, whole_matches DESC, required_matches DESC, score DESC")


def name_rank_clauses(
        node: str, carry: str, words: str = "$search_words") -> str:
    """
    WITH clauses ranking how well `node` (an Officer, Agency or Unit) matches
    the search `words`, keeping the variables in `carry` (which include
    `node`). They add:

    name_tier
        1 - every word is a whole word of the name and the words cover the
            whole name (an officer's first and last name; an agency's or
            unit's full name), in any order: "Rivera Anthony";
        2 - every word starts a word of the name: "Ant Riv", or
            "Anthony Rivera" for Marcus Anthony Rivera;
        3 - only some of the words match.
    whole_matches
        How many of the words are whole words of the name.
    required_matches
        How many words of the first and last name (or the agency's or unit's
        name) the search covers, so "Anthony M Rivera" puts Anthony Rivera
        ahead of Anthony M Angelos.

    Sort with NAME_RANK_ORDER.
    """
    first, middle, last, suffix, name = (
        _words_cypher(f"{node}.{prop}")
        for prop in ("first_name", "middle_name", "last_name", "suffix",
                     "name"))
    return f"""
    WITH {carry},
        CASE WHEN {node}:Officer THEN {first} + {last}
            ELSE {name} END AS required_words,
        CASE WHEN {node}:Officer THEN {first} + {middle} + {last} + {suffix}
            ELSE {name} END AS name_words
    WITH {carry},
        size([search_word IN {words} WHERE search_word IN name_words])
            AS whole_matches,
        size([required IN required_words WHERE required IN {words}])
            AS required_matches,
        CASE
            WHEN all(search_word IN {words} WHERE search_word IN name_words)
                AND all(required IN required_words WHERE required IN {words})
                THEN 1
            WHEN all(search_word IN {words} WHERE any(
                name_word IN name_words
                WHERE name_word STARTS WITH search_word))
                THEN 2
            ELSE 3
        END AS name_tier
    """


def officer_lookup_params(term: str | None, strategy: str) -> dict:
    """
    Query parameters for an officer-list search box whose text was classified
    as a "name", "badge" or "ambiguous" search. `name_query` and
    `badge_query` are left out when the text has nothing searchable.
    """
    words = tokenize(term)
    params = {"search_words": []}
    if not words:
        return params
    if strategy in ("name", "ambiguous"):
        params["search_words"] = words
        params["name_query"] = build_prefix_query(term)
    if strategy in ("badge", "ambiguous"):
        params["badge_query"] = build_exact_query(term)
    return params


def officer_list_ranking(params: dict, carry: str) -> tuple[str, str]:
    """WITH clauses and ORDER BY keys for an officer list: by name match when
    names were searched, otherwise by search score."""
    if params.get("search_words"):
        return name_rank_clauses("o", carry), NAME_RANK_ORDER
    return "", "score DESC"
