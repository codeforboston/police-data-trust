import { useState } from "react"
import { FormProvider, useForm } from "react-hook-form"

import { useAuth, useSearch } from "../../helpers"
import { IToggleOptions, searchPanelInputs, SearchTypes } from "../../models"
import {
  FormLevelError,
  PrimaryButton,
  PrimaryInput,
  SecondaryInput,
  ToggleBox
} from "../../shared-components"
import styles from "./search.module.css"
import SecondaryInputStories from "../../shared-components/secondary-input/secondary-input.stories"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faEdit } from "@fortawesome/free-solid-svg-icons"

const { searchPanelContainer, searchForm } = styles

interface SearchPanelProps {
  toggleOptions: IToggleOptions[]
  setToggleOptions: Function
}

export const SearchPanel = (props: SearchPanelProps) => {
  const form = useForm()
  const { searchIncidents } = useSearch()
  const { accessToken } = useAuth()

  const [errorMessage, setErrorMessage] = useState("")
  const [formInputs, setFormInputs] = useState(searchPanelInputs.incidents)
  const [isLoading, setIsLoading] = useState(false)
  const { toggleOptions, setToggleOptions } = props

  const toggleFormInputs = (e: any) => {
    const updatedToggleOptions = toggleOptions.map(({ type, value }) => {
      return { type, value: !value }
    })
    setToggleOptions(updatedToggleOptions)
    setFormInputs(searchPanelInputs[e.target.value as SearchTypes])
  }

  async function onSubmit({ location, dateEnd, dateStart, description, source }: any) {
    setIsLoading(true)
    try {
      await searchIncidents({ accessToken, description, dateEnd, location, dateStart, source })
    } catch (e) {
      console.error("Unexpected search error", e)
      setErrorMessage("Something went wrong. Please try again.")
      
      /* # TODO: Add error handling when a 401 is recieved. Redirect to login */
    }
    setIsLoading(false)
  }

  return (
    <section className={searchPanelContainer}>
      <FormProvider {...form}>
        <form className={searchForm} onSubmit={form.handleSubmit(onSubmit)}>
          <ToggleBox
            title="I am searching for..."
            options={toggleOptions}
            onChange={toggleFormInputs}
          />
          <fieldset>
            <legend className="screenReaderOnly">Search Criteria</legend>
            {!!formInputs.length &&
              formInputs.map((inputName) => (
                <PrimaryInput isRequired={false} key={inputName} inputName={inputName} />
              ))}
          </fieldset>
          {errorMessage && <FormLevelError errorId="ErrorMessage" errorMessage={errorMessage} />}
          <PrimaryButton loading={isLoading} type="submit">
            <FontAwesomeIcon icon={faEdit} />
            Search
          </PrimaryButton>
        </form>
      </FormProvider>
    </section>
  )
}
