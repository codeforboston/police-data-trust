import * as TG from "@radix-ui/react-toggle-group"
import classNames from "classnames"
import styles from "./yes-no-toggle.module.css"

interface YesNoToggleProps {
  value: "YES" | "NO"
  onChange(...event: any[]): void
}

export default function YesNoToggle({ value, onChange }: YesNoToggleProps) {
  return (
    <TG.Root type="single" value={value} onValueChange={onChange} className={styles.root}>
      <TG.Item
        value={"YES"}
        className={classNames(styles.item, value === "YES" && styles.selected)}>
        Yes
      </TG.Item>
      <TG.Item value={"NO"} className={classNames(styles.item, value === "NO" && styles.selected)}>
        No
      </TG.Item>
    </TG.Root>
  )
}
