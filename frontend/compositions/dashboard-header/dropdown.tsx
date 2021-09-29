import useDropdownMenu from 'react-accessible-dropdown-menu-hook'
import styles from './dropdown.module.css'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faEllipsisV } from "@fortawesome/free-solid-svg-icons"
import Nav from './nav'

export default function Dropdown() {
  const { buttonProps, itemProps, isOpen } = useDropdownMenu(4);

  const { visible, hidden, dropdown } = styles;

  return (
    <div className={dropdown}>
      <button {...buttonProps}>
      <FontAwesomeIcon icon={faEllipsisV} size={"3x"} /></button>
      <div className={isOpen ? visible : hidden } role='menu'>
        <Nav itemProps={itemProps} />
      </div>
    </div>
  )
}