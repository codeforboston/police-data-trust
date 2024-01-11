import { faAngleDoubleDown, faAngleDoubleUp } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { useState } from "react"
import { useMediaQuery } from "react-responsive"
import { SearchPanel } from "../../../compositions"
import { IToggleOptions } from "../../../models"
import styles from "./search-form.module.css"

interface SearchFormProps {
  toggleOptions: IToggleOptions[]
  setToggleOptions: Function
}

export function SearchForm({ toggleOptions, setToggleOptions }: SearchFormProps) {
  const { searchFormContainer, searchFormHeader } = styles
  const [isFormMinimized, setIsFormMinimized] = useState(false)
  const desktop = useMediaQuery({ query: "screen and (min-width: 70em)" })

  const toggleFormMinimized = () => {
    setIsFormMinimized((prev) => !prev)
  }

  return (
    <div className={searchFormContainer}>
      {desktop ? (
        <SearchPanel toggleOptions={toggleOptions} setToggleOptions={setToggleOptions} />
      ) : (
        <>
          <div className={searchFormHeader} onClick={toggleFormMinimized}>
            <h1>Search The Database</h1>
            <FontAwesomeIcon
              icon={isFormMinimized ? faAngleDoubleUp : faAngleDoubleDown}
              size="2x"
            />
          </div>
          {!isFormMinimized && (
            <SearchPanel toggleOptions={toggleOptions} setToggleOptions={setToggleOptions} />
          )}
        </>
      )}
    </div>
  )
}
