"use client"

import * as React from "react"
import Tabs from "@mui/material/Tabs"
import Tab from "@mui/material/Tab"
import Box from "@mui/material/Box"

type DetailTab = {
  label: string
  content: React.ReactNode
  disabled?: boolean
  value?: string | number
}

type TabPanelProps = {
  children?: React.ReactNode
  panelValue: string | number
  value: string | number
}

type DetailsTabsProps = {
  tabs: DetailTab[]
  ariaLabel?: string
  value?: string | number
  onChange?: (newValue: string | number) => void
}

function CustomTabPanel({ children, value, panelValue, ...other }: TabPanelProps) {
  return (
    <div role="tabpanel" hidden={value !== panelValue} {...other}>
      {value === panelValue && <Box sx={{ paddingInline: 0, paddingBlock: 4 }}>{children}</Box>}
    </div>
  )
}

function a11yProps(index: number) {
  return {
    id: `detail-tab-${index}`,
    "aria-controls": `detail-tabpanel-${index}`
  }
}

function panelA11yProps(index: number) {
  return {
    id: `detail-tabpanel-${index}`,
    "aria-labelledby": `detail-tab-${index}`
  }
}

export default function DetailsTabs({
  tabs,
  ariaLabel = "detail tabs",
  value: controlledValue,
  onChange
}: DetailsTabsProps) {
  const [value, setValue] = React.useState<string | number>(tabs[0]?.value ?? 0)

  const activeValue = controlledValue ?? value

  const handleChange = (_event: React.SyntheticEvent, newValue: string | number) => {
    if (controlledValue === undefined) {
      setValue(newValue)
    }
    onChange?.(newValue)
  }

  return (
    <Box sx={{ width: "100%" }}>
      <Box>
        <Tabs
          value={activeValue}
          onChange={handleChange}
          textColor="secondary"
          indicatorColor="secondary"
          aria-label={ariaLabel}
        >
          {tabs.map((tab, index) => (
            <Tab
              key={tab.label}
              label={tab.label}
              value={tab.value ?? index}
              disabled={tab.disabled}
              {...a11yProps(index)}
              sx={{ textTransform: "none" }}
            />
          ))}
        </Tabs>
      </Box>

      {tabs.map((tab, index) => (
        <CustomTabPanel
          key={tab.label}
          value={activeValue}
          panelValue={tab.value ?? index}
          {...panelA11yProps(index)}
        >
          {tab.content}
        </CustomTabPanel>
      ))}
    </Box>
  )
}
