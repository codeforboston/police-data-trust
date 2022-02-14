import { ReactElement } from "react"

interface Tooltips {
  content: (string | (() => ReactElement))[]
}

export enum TooltipTypes {
  VIEWER = "viewerAccounts",
  INCIDENTS = "policeIncidents",
  DATETIME = "dateTime",
  USEFORCE = "useOfForce",
  KEYWORD = "keyWord"
}

export enum TooltipIcons {
  QUESTION = "question",
  INFO = "info"
}

export const tooltipContent: { [key in TooltipTypes]: Tooltips } = {
  [TooltipTypes.VIEWER]: {
    content: [
      "A Viewer account allows you to see data that is publically available.",
      "Once registered, you may optionally apply to see legally protected data through a Passport account"
    ]
  },
  [TooltipTypes.INCIDENTS]: {
    content: [
      "This dropdown menu supplies a list of legal descriptions for known, potential incidents.",
      "Please review this brief legal explainer for further clarification.",
      "We apologize for any unintentional omissions, if you identify one please alert our development team."
    ]
  },
  [TooltipTypes.DATETIME]: {
    content: [
      "Dates are presented in Month-Day-Year format",
      "Times are written in 24-hour format",
      "Any Tildes (~) indicate approximations"
    ]
  },
  [TooltipTypes.USEFORCE]: {
    content: [
      "Use of Force refers to the continuum of violence that may be used in an incident",
      "For more info, view our Use of Force explainer"
    ]
  },
  [TooltipTypes.KEYWORD]: {
    content: [
      "Key words will look for matching words in any column in the database, including names, locations, and descriptions"
    ]
  }
}
