import React, {FC, useState} from "react";
import styles from "./toggle-dropdown.module.css"

interface ToggleDropDownProps{
    title: string
    options: string[]

}

export const ToggleDropDown: FC<ToggleDropDownProps> = ({title, options}) => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleDropDown = () =>{
        setIsOpen(!isOpen)
    }
    return(
        <div className = {styles.togglebutton}>
            <button onClick={toggleDropDown}>{title}</button>
            {isOpen && (
                <div className = {styles.popup}>
                    <ul>
                        {options.map((option,index)=>(
                            <li key = {index}>{option}</li>
                        ))}
                    </ul>
                </div>  
            )}

        </div>
    )
}


