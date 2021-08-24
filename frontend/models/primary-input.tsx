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

const passwordRgx: RegExp = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*d)(?=.*[^a-zA-Zds]).{8,}$")
const nameRgx: RegExp = new RegExp("^[' -]*[a-z]+[a-z' -]+$", "i")

export const primaryInputValidation: { [key in PrimaryInputNames]: primaryInputValidationFormat } =
  {
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
      pattern: new RegExp("^[a-z0-9_.-]+@([a-z0-9_-]+.)+[a-z]{2,4}$", "i"),
      inputType: "email"
    },
    [PrimaryInputNames.PHONE_NUMBER]: {
      errorMessage: "A phone number is required",
      pattern: new RegExp("^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-s./0-9]*$"),
      inputType: "tel"
    },
    [PrimaryInputNames.CREATE_PASSWORD]: {
      errorMessage: "Please enter a valid password",
      pattern: passwordRgx,
      inputType: "password"
    },
    [PrimaryInputNames.CONFIRM_PASSWORD]: {
      errorMessage: "Passwords do not match",
      pattern: passwordRgx,
      inputType: "text"
    },
    [PrimaryInputNames.LOGIN_PASSWORD]: {
      errorMessage: "A password is required",
      pattern: passwordRgx,
      inputType: "password"
    },
    [PrimaryInputNames.STREET_ADDRESS]: {
      errorMessage: "A street address is required",
      pattern: /\d+\s[a-z'-]{2,}\s[a-z'-]{2,}\s?[a-z\d'\.\-\s#]*/i,
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
