import { IconProp } from "@fortawesome/fontawesome-svg-core"
import { faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons"

interface passwordToggleView {
  icon: IconProp
  isHidden: boolean
  text: string
}

export const passwordToggleViews: { [key: string]: passwordToggleView } = {
  showView: { icon: faEye, isHidden: true, text: "Show password" },
  hideView: { icon: faEyeSlash, isHidden: false, text: "Hide password" }
}
