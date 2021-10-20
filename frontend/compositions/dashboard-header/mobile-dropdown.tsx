import styles from "./mobile-dropdown.module.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faEllipsisV } from "@fortawesome/free-solid-svg-icons"
import Nav from "./nav"
import { DropdownProps } from "../../models/nav-dropdown"

export default function MobileDropdown({ buttonProps, itemProps, isOpen }: DropdownProps) {
  const { visible, hidden, dropdown } = styles

  return (
    <div className={dropdown}>
      <button {...buttonProps}>
        <FontAwesomeIcon icon={faEllipsisV} size={"3x"} />
      </button>
      <div className={isOpen ? visible : hidden} role="menu">
        <Nav itemProps={itemProps} />
      </div>
    </div>
  )
}
