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

interface EnrollmentResponseText {
  title: string
  message: string[]
  returnLink?: string
  returnText?: string
}

// TODO: specify how many is XX days!
export const successResponseMessage: { [key in EnrollmentTypes]: EnrollmentResponseText } = {
  [EnrollmentTypes.VIEWER]: {
    title: "Success!",
    message: [
      "You have been successfully registered as a Viewer",
      "**Please check your email to confirm your registration**",
      "The confirmation e-mail will direct you to a new login screen",
      "**If you need access to legally protected data,** you are also invited to apply for a **Passport Account** upon log in."
    ]
  },
  [EnrollmentTypes.PASSPORT]: {
    title: "Success!",
    message: [
      "You have successfully submitted an application for a Passport account",
      "**Please check your email over the next few days**",
      "You can expect to receive a decision in XX days with further instructions. In the meantime, you may continue to explore all public data."
    ],
    returnLink: AppRoutes.DASHBOARD,
    returnText: "Return to dashboard"
  }
}
