interface InputValidation {
  errorMessageText: string,
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

export const inputValidation: { [key in EnrollmentInputNames]: InputValidation } = {
  [EnrollmentInputNames.FIRST_NAME]: {
    errorMessageText: 'A name requires 2+ letters',
    pattern: nameRgx,
    inputType: 'text'
  },
  [EnrollmentInputNames.LAST_NAME]: {
    errorMessageText: 'A name requires 2+ letters',
    pattern: nameRgx,
    inputType: 'text'
  },
  [EnrollmentInputNames.EMAIL_ADDRESS]: {
    errorMessageText: 'Please enter a valid email address',
    pattern: new RegExp('^[a-z0-9_\.\-]+@([a-z0-9_\-]+\.)+[a-z]{2,4}$', 'i'),
    inputType: 'email'
  },
  [EnrollmentInputNames.PHONE_NUMBER]: {
    errorMessageText: 'Please enter a valid phone number',
    pattern: new RegExp('^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.\/0-9]*$'),
    inputType: 'tel'
  },
  [EnrollmentInputNames.CREATE_PASSWORD]: {
    errorMessageText: 'Please enter a valid password',
    pattern: passwordRgx,
    inputType: 'password'
  },
  [EnrollmentInputNames.CONFIRM_PASSWORD]: {
    errorMessageText: 'Passwords do not match',
    pattern: passwordRgx,
    inputType: 'text'
  },
  [EnrollmentInputNames.LOGIN_PASSWORD]: {
    errorMessageText: 'A password is required',
    pattern: passwordRgx,
    inputType: 'password'
  },
  [EnrollmentInputNames.STREET_ADDRESS]: {
    errorMessageText: 'A street address is required',
    pattern: /.+/,
    inputType: 'text'
  }, 
  [EnrollmentInputNames.CITY_TOWN]: {
    errorMessageText: 'A city or town is required',
    pattern: /.+/,
    inputType: 'text'
  },
  [EnrollmentInputNames.ZIP_CODE]: {
    errorMessageText: 'Zipcode is required',
    pattern: /.+/,
    inputType: 'number'
  }
}