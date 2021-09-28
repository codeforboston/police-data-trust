interface primaryInputValidationFormat {
  errorMessage: string
  pattern: RegExp
  inputType: string
}

export enum PrimaryInputNames {
  FIRST_NAME = "firstName",
  LAST_NAME = "lastName",
  EMAIL_ADDRESS = "emailAddress",
  PHONE_NUMBER = "phoneNumber",
  CREATE_PASSWORD = "createPassword",
  CONFIRM_PASSWORD = "confirmPassword",
  LOGIN_PASSWORD = "loginPassword",
  STREET_ADDRESS = "streetAddress",
  CITY_TOWN = "cityOrTown",
  ZIP_CODE = "zipCode"
}

const passwordRgx: RegExp = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z\d\s]).{8,}$/

const nameRgx: RegExp = new RegExp("^[' -]*[a-z]+[a-z' -]+$", "i")

export const primaryInputValidation = {
  [PrimaryInputNames.FIRST_NAME]: {
    errorMessage: "A name requires 2+ letters",
    pattern: nameRgx,
    inputType: "text"
  },
  [PrimaryInputNames.LAST_NAME]: {
    errorMessage: "A name requires 2+ letters",
    pattern: nameRgx,
    inputType: "text"
  },
  [PrimaryInputNames.EMAIL_ADDRESS]: {
    errorMessage: "Please enter a valid email",
    pattern: /^[a-z0-9_.-]+@[a-z0-9_.-]+\.[a-z]{2,4}$/i,
    inputType: "email"
  },
  [PrimaryInputNames.PHONE_NUMBER]: {
    errorMessage: 'A phone number is required, formatted as "123 456 7890"',
    pattern: /\d{3} \d{3} \d{4}/,
    inputType: "tel"
  },
  [PrimaryInputNames.CREATE_PASSWORD]: {
    errorMessage:
      "Please enter a password that contains a digit, uppercase letter, lowercase letter, special symbol, and is at least 8 characters long",
    pattern: passwordRgx,
    inputType: "password"
  },
  [PrimaryInputNames.CONFIRM_PASSWORD]: {
    errorMessage: "Please confirm your password",
    pattern: /.+/,
    inputType: "password"
  },
  [PrimaryInputNames.LOGIN_PASSWORD]: {
    errorMessage: "A password is required",
    pattern: /.+/,
    inputType: "password"
  },
  [PrimaryInputNames.STREET_ADDRESS]: {
    errorMessage: "A street address is required",
    pattern: /.+/,
    inputType: "text"
  },
  [PrimaryInputNames.CITY_TOWN]: {
    errorMessage: "A city or town is required",
    pattern: /[a-z' -]{3,}/i,
    inputType: "text"
  },
  [PrimaryInputNames.ZIP_CODE]: {
    errorMessage: "5 digits required",
    pattern: new RegExp("^[0-9]{5}$"),
    inputType: "number"
  }
}
