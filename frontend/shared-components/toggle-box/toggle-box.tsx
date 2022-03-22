import React, { FC, useState } from "react"
import { capitalizeFirstChar } from "../../helpers"
import styles from "./toggle-box.module.css"

interface ToggleBoxProps {
  title: string
  options: { type: string; value: boolean }[]
  onChange: (e: any) => void
}
export const ToggleBox: FC<ToggleBoxProps> = ({ title, options, onChange }) => {
  return (
    <div className={styles.searchToggle}>
      <fieldset>
        <legend>{title}</legend>
        {options.length > 0 &&
          options.map(({ type, value }, i) => (
            <div key={`toggle-input-${i}`}>
              <input
                id={type + "-radio"}
                key={i}
                type="radio"
                name="search-type"
                value={type}
                checked={value}
                onChange={onChange}
              />
              <label htmlFor={type + "-radio"}>{capitalizeFirstChar(type)}</label>
            </div>
          ))}
      </fieldset>
    </div>
  )
}
