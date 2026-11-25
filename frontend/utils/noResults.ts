type MaybeExact = { exact_match?: boolean | null }

/**
 * The message for a search with no exact match:
 * "No results found for Christopher West. Try a new search term." without filters, or
 * "... Clear filters and try again." with them. Without a search term (filters only),
 * the term is left out.
 */
export function noResultsMessage(term: string, hasFilters: boolean): string {
  const shownTerm = term.trim().replace(/\s+/g, " ").replace(/\.+$/, "")
  const nextStep = hasFilters ? "Clear filters and try again." : "Try a new search term."
  return shownTerm
    ? `No results found for ${shownTerm}. ${nextStep}`
    : `No results found. ${nextStep}`
}

/**
 * True when results came back but none of them is an exact match. Exact matches are
 * listed first, so the first page settles it; a missing flag (no search text) is never
 * counted as "no exact match".
 */
export function hasNoExactMatch(results: MaybeExact[]): boolean {
  return results.length > 0 && results.every((result) => result.exact_match === false)
}
