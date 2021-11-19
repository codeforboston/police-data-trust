function capitalizeFirstChar(inputString: string): string {
  return inputString.charAt(0).toUpperCase() + inputString.toLowerCase().slice(1)
}

function getTitleCaseFromCamel(camelCase: string): string {
  const spacedTitleCase: string =
    camelCase
      .match(/(^[a-z]+)|[A-Z][a-z]+/g)
      ?.map(capitalizeFirstChar)
      ?.join(" ") || camelCase
  return spacedTitleCase
}

export { capitalizeFirstChar, getTitleCaseFromCamel }

export const formatDate = (unixDate: number): string => new Date(unixDate).toLocaleDateString()
