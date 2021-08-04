import { AppRoutes } from '../models'

interface EnrollmentSuccessText {
  title: string,
  message: string
}

interface EnrollmentErrorText {
  title: string,
  message: string,
  helpLink: string,
  helpText: string,
  returnLink: string,
  returnText: string
}

export enum EnrollmentTypes {
  VIEWER = 'viewer',
  PASSPORT = 'passport'
}

export const enrollmentSuccessText: { [key in EnrollmentTypes]: EnrollmentSuccessText} = {
  [EnrollmentTypes.VIEWER]: {
    title: 'Success!',
    message: 'You have been successfully registered as a Viewer\n*Please check your email to confirm your registration*\nThe confirmation email will direct you to a new login screen.\n*If you need access to legally protected data,* you are also invited to apply for a *Passport Account* upon login.'
  },
  [EnrollmentTypes.PASSPORT]: {
    title: 'Success!',
    message: 'You have been successfully submitted an application for a Passport account\n*Please check your email to confirm your registration*\nYou can expect to receive a decision in XX days with further instructions. In the meantime, you may continue to explore all public data.'
  }
}

export const enrollmentErrorText:  {[key in EnrollmentTypes]: EnrollmentErrorText} = {
  [EnrollmentTypes.VIEWER]: {
    title: 'Something went wrong...',
    message: 'We weren\'t able to complete your registration.\n*Please come back and try again later*\nIf the problem persists, please ',
    helpLink: 'https://github.com/codeforboston/police-data-trust',
    helpText: 'alert our development team',
    returnLink: AppRoutes.LOGIN,
    returnText: 'Return to login'
  },
  [EnrollmentTypes.PASSPORT]: {
    title: 'Something went wrong...',
    message: 'We weren\'t able to complete your registration.\n*Please come back and try again later*\nIf the problem persists, please ',
    helpLink: 'https://github.com/codeforboston/police-data-trust',
    helpText: 'alert our development team',
    returnLink: AppRoutes.LOGIN,
    returnText: 'Return to login'
  }

}