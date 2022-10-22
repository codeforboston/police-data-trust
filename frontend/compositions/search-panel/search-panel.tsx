import { useState } from "react"
import { FormProvider, useForm } from "react-hook-form"

import { useAuth, useSearch } from "../../helpers"
import { searchPanelInputs, SearchTypes, ToggleOptions } from "../../models"
import { FormLevelError, PrimaryButton, PrimaryInput, ToggleBox } from "../../shared-components"
import styles from "./search.module.css"

const { searchPanelContainer, searchForm } = styles

export const SearchPanel = () => {
  const form = useForm()
  const { searchIncidents } = useSearch()
  const { accessToken } = useAuth()

  const [errorMessage, setErrorMessage] = useState("")
  const [formInputs, setFormInputs] = useState(searchPanelInputs.incidents)
  const [isLoading, setIsLoading] = useState(false)
  const [toggleOptions, setToggleOptions] = useState(
    new ToggleOptions("incidents", "officers").options
  )

  const toggleFormInputs = (e: any) => {
    const updatedToggleOptions = toggleOptions.map(({ type, value }) => {
      return { type, value: !value }
    })
    setToggleOptions(updatedToggleOptions)
    setFormInputs(searchPanelInputs[e.target.value as SearchTypes])
  }

  async function onSubmit({ location, startTime, endTime, description }: any) {
    setIsLoading(true)
    try {
      await searchIncidents({ accessToken, description, endTime, location, startTime })
    } catch (e) {
      console.error("Unexpected search error", e)
      setErrorMessage("Something went wrong. Please try again.")
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
            Search
          </PrimaryButton>
        </form>
      </FormProvider>
    </section>
  )
}
