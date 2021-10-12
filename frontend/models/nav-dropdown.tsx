interface ItemProps {
  onKeyDown: (e: React.KeyboardEvent<HTMLAnchorElement>) => void
  tabIndex: number
  role: string
  ref: React.RefObject<HTMLAnchorElement>
}

interface ButtonProps
  extends Pick<
    React.DetailedHTMLProps<React.ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement>,
    "onKeyDown" | "onClick" | "tabIndex" | "role" | "aria-haspopup" | "aria-expanded"
  > {
  ref: React.RefObject<HTMLButtonElement>
}

export interface DropdownProps {
  itemProps: ItemProps[]
  buttonProps?: ButtonProps
  isOpen?: boolean
}
