function capitalizeFirstChar(inputString: string): string {
  return inputString.charAt(0).toUpperCase() + inputString.slice(1) 
}

function getTitleCaseFromCamel(camelCase: string): string {
  const spacedCamelCase: string = camelCase.match(/(^[a-z]+)|[A-Z][a-z]+/g)?.join(' ') || camelCase
  return capitalizeFirstChar(spacedCamelCase)
}

export{ getTitleCaseFromCamel }