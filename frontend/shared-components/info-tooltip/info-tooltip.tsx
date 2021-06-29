import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faQuestionCircle } from '@fortawesome/free-regular-svg-icons'
import React from 'react' 
import styles from './info-tooltip.module.css'
import { tooltipContent, TooltipTypes } from '../../models'

interface InfoTooltipProps { type: TooltipTypes }
export default function InfoTooltip({ type }: InfoTooltipProps) {
  const { tooltipContainer, tooltipIcon, tooltip } = styles
  
  const ariaLabel: string = `Learn more about ${type}`
  const tooltipBodyId: string = `${type}Tooltip`
  const { content } = tooltipContent[type]

  return (
    <div 
      className={tooltipContainer}
      aria-label={ariaLabel} 
      aria-describedby={tooltipBodyId}
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
