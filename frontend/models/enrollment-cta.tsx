import { AppRoutes } from '../models'

interface CTAText {
  description: string, 
  linkText: string, 
  linkPath: AppRoutes 
}

export enum CTATypes {
  LOGIN = 'login',
  REGISTER = 'register',
  DASHBOARD = 'dashboard'
}

export const enrollmentCTAText: { [key in CTATypes]: CTAText} = {
  [CTATypes.LOGIN]: {
    description: 'Do you already have an account with us?',
    linkText: 'Login instead',
    linkPath: AppRoutes.LOGIN
  },
  [CTATypes.REGISTER]: {
    description: 'New to the National Police Data Coalition?',
    linkText: 'Register for an account',
    linkPath: AppRoutes.REGISTER
  },
  [CTATypes.DASHBOARD]: {
    description: 'Is the publically available data sufficient for your needs?',
    linkText: 'Return to dashboard',
    linkPath: AppRoutes.DASHBOARD
  }
}