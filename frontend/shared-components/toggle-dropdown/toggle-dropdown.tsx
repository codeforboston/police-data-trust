import React, {FC, useState} from "react";
import styles from "./toggle-dropdown.module.css"
import {Select} from "../../shared-components"

interface ToggleDropDownProps{
    className?: string
    title: string,
    editChange: Function
    options: any[]

}

export default function ToggleDropDown({className, title, editChange, options}: ToggleDropDownProps) {
    const [isOpen, setIsOpen] = useState(false);

    const toggleDropDown = () =>{
        setIsOpen(!isOpen)
    }
    return(
        <Select.Root>
            <Select.Trigger className={className}>
                <Select.Value placeholder = {title}/>
            </Select.Trigger>
            <Select.Content>
                <Select.Group>
                    {options.map((option) =>(
                        <Select.Item key={option.item} 
                        value = {option.text} 
                        onClick={()=>editChange(option.item)}>{option.text}</Select.Item>
                    ))} 
                </Select.Group>
            </Select.Content>
          
    
        </Select.Root>
 
    )
}


