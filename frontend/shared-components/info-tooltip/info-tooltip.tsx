import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faQuestionCircle } from '@fortawesome/free-regular-svg-icons'
import React from 'react' 
import styles from './info-tooltip.module.css'
import { getTitleCaseFromCamel } from '../../helpers/syntax-helper'
import { tooltipContent, TooltipTypes } from '../../models'

interface InfoTooltipProps { type: TooltipTypes }
export default function InfoTooltip({ type }: InfoTooltipProps) {
  const { tooltipContainer, tooltipIcon, tooltip } = styles
  
  const ariaLabel: string = `Learn more about ${getTitleCaseFromCamel(type)}`
  const tooltipBodyId: string = `${type}Tooltip`
  const { content } = tooltipContent[type]

  return (
    <div 
      className={tooltipContainer}
      aria-label={ariaLabel} 
      aria-describedby={tooltipBodyId}
      role="tooltip"
      tabIndex={0}
    >
      <FontAwesomeIcon 
        className={tooltipIcon}
        aria-hidden={true}
        icon={faQuestionCircle} 
      />
      <div id={tooltipBodyId} className={tooltip}>
        {content.map(sentence => <p key={sentence.slice(0,5)}>{sentence}</p>)}
      </div>
    </div>
  )
}
// TODO: 1) Convert relevant text portions in INCIDENTS content to new-tab links
// 2) Adjust styling so that it's responsive to text length & doesn't mess w/mobile page layout