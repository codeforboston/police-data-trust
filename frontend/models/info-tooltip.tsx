interface Tooltips {
  content: string[]
}

export enum TooltipTypes {
  VIEWER = "viewerAccounts",
  INCIDENTS = "policeIncidents"
}

export const tooltipContent: { [key in TooltipTypes]: Tooltips } = {
  [TooltipTypes.VIEWER]: {
    content: [
      'A Viewer account allows you to see data that is publically available.',
      'Once registered, you may optionally apply to see legally protected data through a Passport account'
    ]
  },
  [TooltipTypes.INCIDENTS]: {
    content: [
      'This dropdown menu supplies a list of legal descriptions for known, potential incidents.',
      'Please review this brief legal explainer for further clarification.',
      'We apologize for any unintentional omissions, if you identify one please alert our development team.'
    ]
  } 
}