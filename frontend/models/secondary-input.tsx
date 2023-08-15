export enum SecondaryInputNames {
  SOURCE = "source"
}

const passwordRgx: RegExp = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z\d\s]).{8,}$/
const nameRgx: RegExp = new RegExp("^[' -]*[a-z]+[a-z' -]+$", "i")
const anyString: RegExp = new RegExp("[sS]*")
const phoneNumberRgx: RegExp = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/
const emailRgx: RegExp = /^[a-z0-9_.-]+@[a-z0-9_.-]+\.[a-z]{2,4}$/i
const urlRgx: RegExp = /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/

export const secondaryInputValidation = {
  [SecondaryInputNames.SOURCE]: {
    errorMessage: "A badge number requires 2+ letters",
    pattern: anyString,
    inputType: "text"
  }
}
