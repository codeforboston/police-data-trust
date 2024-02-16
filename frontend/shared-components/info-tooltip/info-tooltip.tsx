import React, { ReactElement } from "react"
import { Tooltip as ReactTooltip } from "react-tooltip"
import styles from "./info-tooltip.module.css"
import { getTitleCaseFromCamel } from "../../helpers"
import { tooltipContent, TooltipTypes, TooltipIcons } from "../../models"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faQuestionCircle } from "@fortawesome/free-regular-svg-icons"
import { faInfoCircle, IconDefinition } from "@fortawesome/free-solid-svg-icons"

const CONTENT_SPLIT = ":::::"

function getTipIcon(icon: TooltipIcons): IconDefinition {
  return icon === TooltipIcons.INFO ? faInfoCircle : faQuestionCircle
}

export interface InfoTooltipProps {
  type: TooltipTypes
  icon?: TooltipIcons
  iconSize?: any
}
export default function InfoTooltip({
  type,
  icon = TooltipIcons.QUESTION,
  iconSize = "sm"
}: InfoTooltipProps) {
  const { tooltipContainer, tooltipIcon, tooltip } = styles
  const ariaLabel: string = `Learn more about ${getTitleCaseFromCamel(type)}`
  const tooltipBodyId: string = `${type}Tooltip`
  const { content } = tooltipContent[type]

  const display = (x: string | (() => ReactElement)) => {
    return typeof x === "string" ? <p key={x.slice(0, 5)}>{x}</p> : x()
  }

  return (
    <div
      className={tooltipContainer}
      aria-label={ariaLabel}
      aria-describedby={tooltipBodyId}
      role="tooltip"
      tabIndex={0}>
      <FontAwesomeIcon
        className={tooltipIcon}
        aria-hidden={true}
        icon={getTipIcon(icon)}
        size={iconSize}
        data-tooltip-id="table-column-tooltip"
        data-tooltip-content={content.join(CONTENT_SPLIT)}
      />
      <ReactTooltip
        id="table-column-tooltip"
        className={tooltip}
        render={({ content }) => {
          const contentArr = content?.split(CONTENT_SPLIT)

          return (
            <div id={tooltipBodyId}>{contentArr?.map((contentItem) => display(contentItem))}</div>
          )
        }}
      />
    </div>
  )
}
// TODO: 1) Convert relevant text portions in INCIDENTS content to new-tab links
