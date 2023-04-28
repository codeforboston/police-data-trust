export enum PrimaryInputNames {
  BADGE_NUMBER = "badgeNumber",
  CITY_TOWN = "cityOrTown",
  CONFIRM_PASSWORD = "confirmPassword",
  CREATE_PASSWORD = "createPassword",
  DATE = "date",
  DATE_END = "dateEnd",
  DATE_START = "dateStart",
  EMAIL_ADDRESS = "emailAddress",
  FIRST_NAME = "firstName",
  INCIDENT_TYPE = "incidentType",
  KEY_WORDS = "keyWords",
  LAST_NAME = "lastName",
  LOCATION = "location",
  LOGIN_PASSWORD = "loginPassword",
  OFFICER_NAME = "officerName",
  PHONE_NUMBER = "phoneNumber",
  STREET_ADDRESS = "streetAddress",
  ZIP_CODE = "zipCode"
}

const passwordRgx: RegExp = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z\d\s]).{8,}$/
const nameRgx: RegExp = new RegExp("^[' -]*[a-z]+[a-z' -]+$", "i")
const anyString: RegExp = new RegExp("[sS]*")
const phoneNumberRgx: RegExp  = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/


export const primaryInputValidation = {
  [PrimaryInputNames.BADGE_NUMBER]: {
    errorMessage: "A badge number requires 2+ letters",
    pattern: anyString,
    inputType: "text"
  },
  [PrimaryInputNames.CITY_TOWN]: {
    errorMessage: "A city or town is required",
    pattern: /[a-z' -]{3,}/i,
    inputType: "text"
  },
  [PrimaryInputNames.CONFIRM_PASSWORD]: {
    errorMessage: "Please confirm your password",
    pattern: /.+/,
    inputType: "password"
  },
  [PrimaryInputNames.CREATE_PASSWORD]: {
    errorMessage:
      "Please enter a password that contains a digit, uppercase letter, lowercase letter, special symbol, and is at least 8 characters long",
    pattern: passwordRgx,
    inputType: "password"
  },
  [PrimaryInputNames.DATE]: {
    errorMessage: "Date",
    pattern: anyString,
    inputType: "date"
  },
  [PrimaryInputNames.DATE_START]: {
    errorMessage: "Enter a date",
    pattern: anyString,
    inputType: "date"
  },
  [PrimaryInputNames.DATE_END]: {
    errorMessage: "Enter a date",
    pattern: anyString,
    inputType: "date"
  },
  [PrimaryInputNames.EMAIL_ADDRESS]: {
    errorMessage: "Please enter a valid email",
    pattern: /^[a-z0-9_.-]+@[a-z0-9_.-]+\.[a-z]{2,4}$/i,
    inputType: "email"
  },
  [PrimaryInputNames.FIRST_NAME]: {
    errorMessage: "A name requires 2+ letters",
    pattern: nameRgx,
    inputType: "text"
  },
  [PrimaryInputNames.INCIDENT_TYPE]: {
    errorMessage: "A name requires 2+ letters",
    pattern: anyString,
    inputType: "text"
  },
  [PrimaryInputNames.LAST_NAME]: {
    errorMessage: "A name requires 2+ letters",
    pattern: nameRgx,
    inputType: "text"
  },
  [PrimaryInputNames.PHONE_NUMBER]: {
    errorMessage: 'A valid phone number is required',
    pattern: phoneNumberRgx,
    inputType: "tel"
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
  [PrimaryInputNames.ZIP_CODE]: {
    errorMessage: "5 digits required",
    pattern: new RegExp("^[0-9]{5}$"),
    inputType: "number"
  },
  [PrimaryInputNames.OFFICER_NAME]: {
    errorMessage: "A name requires 2+ letters",
    pattern: nameRgx,
    inputType: "text"
  },
  [PrimaryInputNames.LOCATION]: {
    errorMessage: "A location requires 2+ letters",
    pattern: nameRgx,
    inputType: "text"
  },
  [PrimaryInputNames.KEY_WORDS]: {
    errorMessage: "Enter a valid term",
    pattern: anyString,
    inputType: "text"
  }
}

export enum SearchTypes {
  INCIDENTS = "incidents",
  OFFICERS = "officers"
}

export const searchPanelInputs: { [key in SearchTypes]: PrimaryInputNames[] } = {
  [SearchTypes.INCIDENTS]: [
    PrimaryInputNames.LOCATION,
    PrimaryInputNames.INCIDENT_TYPE,
    PrimaryInputNames.DATE
  ],
  [SearchTypes.OFFICERS]: [
    PrimaryInputNames.OFFICER_NAME,
    PrimaryInputNames.LOCATION,
    PrimaryInputNames.BADGE_NUMBER
  ]
}
