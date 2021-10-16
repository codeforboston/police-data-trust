export enum SearchResultsTypes {
  NOSEARCHPARAMS = "nosearch",
  NORESULTS = "noresults"
}

export const alertContent: { [key in SearchResultsTypes]: string } = {
  [SearchResultsTypes.NOSEARCHPARAMS]: "You must provide at least one field",
  [SearchResultsTypes.NORESULTS]: "No matching results found"
}
