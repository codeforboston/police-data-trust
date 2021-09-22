import { AppRoutes } from "./"

interface EnrollmentErrorText {
  statusMessage: string
  returnText: string
  returnPath: string
}

export enum EnrollmentTypes {
  VIEWER = "viewer",
  PASSPORT = "passport"
}

export const enrollmentMessage: { [key in EnrollmentTypes]: EnrollmentErrorText } = {
  [EnrollmentTypes.VIEWER]: {
    statusMessage: "complete your registration",
    returnText: "Return to login",
    returnPath: AppRoutes.LOGIN
  },
  [EnrollmentTypes.PASSPORT]: {
    statusMessage: "submit your application",
    returnText: "Return to dashboard",
    returnPath: AppRoutes.DASHBOARD
  }
}
