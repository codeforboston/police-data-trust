// Name matching for lists searched in the browser (an agency's units). It follows the
// server-side rules in backend/queries/text_search.py, so these lists rank names the
// same way the site's other searches do.

// Characters that split search text and names into words. Apostrophes stay inside
// words (O'Brien).
const WORD_SEPARATORS = '+-!(){}[]^"~*?:\\/|&.,;_'
const escapeForRegExp = (text: string) => text.replace(/[.*+?^${}()|[\]\\/-]/g, "\\$&")
const SEPARATOR_PATTERN = new RegExp(`[\\s${escapeForRegExp(WORD_SEPARATORS)}]+`)
const BOOLEAN_OPERATORS = new Set(["AND", "OR", "NOT"])

/** Lower-cased words of search text, without apostrophes at their edges or AND/OR/NOT. */
export function tokenizeSearch(text: string): string[] {
  return text
    .split(SEPARATOR_PATTERN)
    .map((word) => word.replace(/^'+|'+$/g, "").toLowerCase())
    .filter((word) => word && !BOOLEAN_OPERATORS.has(word.toUpperCase()))
}

/** Lower-cased words of a name. */
export function nameWords(name: string): string[] {
  return name.toLowerCase().split(SEPARATOR_PATTERN).filter(Boolean)
}

export type NameMatch<T> = {
  item: T
  // Every searched word is a whole word of the name, in any order.
  exact_match: boolean
}

/**
 * The items whose name has a word starting with one of the searched words, best match
 * first:
 *   1. every searched word is a whole word and together they cover the whole name;
 *   2. every searched word starts a word of the name;
 *   3. only some of the searched words match.
 * Within each group, more whole-word matches come first, then names in A-Z order.
 */
export function rankByName<T>(
  items: T[],
  term: string,
  getName: (item: T) => string | undefined
): NameMatch<T>[] {
  const words = tokenizeSearch(term)
  if (words.length === 0) {
    return []
  }

  const ranked = items.flatMap((item) => {
    const name = getName(item) ?? ""
    const parts = nameWords(name)
    const startsAWord = (word: string) => parts.some((part) => part.startsWith(word))
    if (!words.some(startsAWord)) {
      return []
    }

    const wholeMatches = words.filter((word) => parts.includes(word)).length
    const requiredMatches = parts.filter((part) => words.includes(part)).length
    const tier =
      wholeMatches === words.length && requiredMatches === parts.length
        ? 1
        : words.every(startsAWord)
          ? 2
          : 3

    return [{ item, name, tier, wholeMatches, requiredMatches }]
  })

  ranked.sort(
    (a, b) =>
      a.tier - b.tier ||
      b.wholeMatches - a.wholeMatches ||
      b.requiredMatches - a.requiredMatches ||
      a.name.localeCompare(b.name)
  )

  return ranked.map(({ item, wholeMatches }) => ({
    item,
    exact_match: wholeMatches === words.length
  }))
}
