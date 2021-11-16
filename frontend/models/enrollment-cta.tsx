import { AppRoutes } from "../models"

interface CallToActionText {
  description?: string
  linkText: string
  linkPath: AppRoutes
}

export enum CallToActionTypes {
  LOGIN = "login",
  REGISTER = "register",
  DASHBOARD = "dashboard",
  FORGOT = "forgot",
  REMEMBER = "remember"
}

export const enrollmentCallToActionText: { [key in CallToActionTypes]: CallToActionText } = {
  [CallToActionTypes.LOGIN]: {
    description: "Do you already have an account with us?",
    linkText: "Login instead",
    linkPath: AppRoutes.LOGIN
  },
  [CallToActionTypes.REGISTER]: {
    description: "New to the National Police Data Coalition?",
    linkText: "Register for an account",
    linkPath: AppRoutes.REGISTER
  },
  [CallToActionTypes.DASHBOARD]: {
    description: "Is the publically available data sufficient for your needs?",
    linkText: "Return to dashboard",
    linkPath: AppRoutes.DASHBOARD
  },
  [CallToActionTypes.FORGOT]: {
    //description: "New to the National Police Data Coalition?",
    linkText: "Forgot your password?",
    linkPath: AppRoutes.FORGOT
  },
  [CallToActionTypes.REMEMBER]: {
    description: "Do you remember you login credentials?",
    linkText: "Return to login",
    linkPath: AppRoutes.LOGIN
  }
}
