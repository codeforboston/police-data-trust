interface enrollmentValidation {
  errorMessage: string,
  pattern: RegExp,
  inputType: string
}

export enum EnrollmentInputNames {
  FIRST_NAME = 'firstName',
  LAST_NAME = 'lastName',
  EMAIL_ADDRESS = 'emailAddress',
  PHONE_NUMBER = 'phoneNumber',
  CREATE_PASSWORD = 'createPassword',
  CONFIRM_PASSWORD = 'confirmPassword',
  LOGIN_PASSWORD = 'loginPassword',
  STREET_ADDRESS = 'streetAddress',
  CITY_TOWN = 'cityOrTown',
  ZIP_CODE = 'zipCode'
}

const passwordRgx: RegExp = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z\d\s]).{8,}$")
const nameRgx: RegExp = new RegExp("^[' -]*[a-z]+[a-z' -]+$", 'i')

export const enrollmentValidation: { [key in EnrollmentInputNames]: enrollmentValidation } = {
  [EnrollmentInputNames.FIRST_NAME]: {
    errorMessage: 'A name requires 2+ letters',
    pattern: nameRgx,
    inputType: 'text'
  },
  [EnrollmentInputNames.LAST_NAME]: {
    errorMessage: 'A name requires 2+ letters',
    pattern: nameRgx,
    inputType: 'text'
  },
  [EnrollmentInputNames.EMAIL_ADDRESS]: {
    errorMessage: 'Please enter a valid email',
    pattern: new RegExp('^[a-z0-9_\.\-]+@([a-z0-9_\-]+\.)+[a-z]{2,4}$', 'i'),
    inputType: 'email'
  },
  [EnrollmentInputNames.PHONE_NUMBER]: {
    errorMessage: 'A phone number is required',
    pattern: new RegExp('^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.\/0-9]*$'),
    inputType: 'tel'
  },
  [EnrollmentInputNames.CREATE_PASSWORD]: {
    errorMessage: 'Please enter a valid password',
    pattern: passwordRgx,
    inputType: 'password'
  },
  [EnrollmentInputNames.CONFIRM_PASSWORD]: {
    errorMessage: 'Passwords do not match',
    pattern: passwordRgx,
    inputType: 'text'
  },
  [EnrollmentInputNames.LOGIN_PASSWORD]: {
    errorMessage: 'A password is required',
    pattern: passwordRgx,
    inputType: 'password'
  },
  [EnrollmentInputNames.STREET_ADDRESS]: {
    errorMessage: 'A street address is required',
    pattern: /\d+\s[a-z'-]{2,}\s[a-z'-]{2,}\s?[a-z\d'\.\-\s#]*/i,
    inputType: 'text'
  }, 
  [EnrollmentInputNames.CITY_TOWN]: {
    errorMessage: 'A city or town is required',
    pattern: /[a-z' -]{3,}/i,
    inputType: 'text'
  },
  [EnrollmentInputNames.ZIP_CODE]: {
    errorMessage: '5 digits required',
    pattern: new RegExp('^[0-9]{5}$'),
    inputType: 'number'
  }
}