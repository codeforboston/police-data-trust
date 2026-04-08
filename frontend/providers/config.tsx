export const getParamKeys = (tab: number) => {
  switch (tab) {
    case 1:
      return ["query"]
    case 2:
      return ["name"]
    case 3:
      return ["name"]
    default:
      return ["query"]
  }
}
