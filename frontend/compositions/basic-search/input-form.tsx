import React, { useState } from "react"
import { FormProvider, useForm, useFormContext } from "react-hook-form"
import { useAuth, useSearch } from "../../helpers"
import { FormLevelError, PrimaryButton } from "../../shared-components"
import sharedStyles from "../../styles/shared.module.css"

const Inputs = {
  Location: "Location",
  StartTime: "Start Date",
  EndTime: "End Date",
  Description: "Description"
}

export function InputForm() {
  const { searchIncidents } = useSearch()
  const form = useForm()
  const [loading, setLoading] = useState(false)
  const [submitError, setSubmitError] = useState(null)
  const { accessToken } = useAuth()

  async function onSubmit(formValues: any) {
    setLoading(true)
    setSubmitError(null)
    try {
      const clean = (x: any) => (!x ? undefined : x)
      await searchIncidents({
        accessToken,
        location: clean(formValues[Inputs.Location]),
        startTime: clean(formValues[Inputs.StartTime]),
        endTime: clean(formValues[Inputs.EndTime]),
        description: clean(formValues[Inputs.Description])
      })
    } catch (e) {
      console.error("Search error", e)
      setSubmitError("Something went wrong. Please try again.")
    }
    setLoading(false)
  }

  return (
    <section style={{ maxWidth: "500px", margin: "1em auto" }}>
      <h1>Search Incidents</h1>
      <FormProvider {...form}>
        <form className={sharedStyles.centerContent} onSubmit={form.handleSubmit(onSubmit)}>
          <Input name={Inputs.Location} placeholder={"Location keyword"} />
          <Input name={Inputs.StartTime} type="date" />
          <Input name={Inputs.EndTime} type="date" />
          <Input name={Inputs.Description} placeholder={"Description keyword"} />
          {submitError && <FormLevelError errorId="submitError" errorMessage={submitError} />}
          <PrimaryButton loading={loading} type="submit">
            Search
          </PrimaryButton>
        </form>
      </FormProvider>
    </section>
  )
}

function Input({ name, type = "text", placeholder }: any) {
  const { register } = useFormContext()
  return (
    <fieldset style={{ display: "flex", alignItems: "center" }}>
      <label>{name}</label>
      <input
        style={{ margin: "10px", flex: "auto" }}
        name={name}
        type={type}
        placeholder={placeholder}
        {...register(name, { required: false })}
      />
    </fieldset>
  )
}
