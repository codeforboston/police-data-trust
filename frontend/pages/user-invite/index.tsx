import React, { useState } from "react"
import { FormProvider, useForm } from "react-hook-form"
import { Logo, PrimaryInput } from "../../shared-components"
import { LogoSizes } from "../../models"
import styles from "./inviting-user.module.css"
import { PrimaryInputNames } from "../../models"
import { apiMode } from "../../helpers/api"
import { ToggleBox } from "../../shared-components"

const paragraph = "Lorem Ipsum is simply dummy text of the printing and typesetting industry.\nLorem Ipsum has been the industry's standard dummy text ever since the 1500s,\nwhen an unknown printer";
const {EMAIL_ADDRESS} = PrimaryInputNames
const defaultEmail = apiMode === "mock" ? "test@example.com" : undefined


const [toggleOptions, setToggleOptions] = useState([
    { type: 'Publisher', value: true },
    { type: 'Admin', value: false },
    { type: 'Member', value: false },
    { type: 'Subscriber', value: false }
    
  ]);
const handleToggleChange = (updatedOptions: React.SetStateAction<{ type: string; value: boolean }[]>) => {
    setToggleOptions(updatedOptions);
    // Additional logic if needed
  };
export default function InviteUser(){
    const form = useForm()
    return(
    <div className={styles.container}>
        <div className= {styles.center}>
            <Logo size = { LogoSizes.LARGE} />
        </div>

        <h1>Inviting a User</h1>
        <p className={styles.paragraph}>
        {paragraph}
        </p>
        <FormProvider {...form}>
        <form>
            <PrimaryInput inputName={EMAIL_ADDRESS} className={styles.email_input}/>
            <ToggleBox title ={"Role"} options={toggleOptions} onChange={handleToggleChange}/>
        </form>
        </FormProvider>
    </div>
    )
}