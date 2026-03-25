"use client"

import * as React from "react"
import Tabs from "@mui/material/Tabs"
import Tab from "@mui/material/Tab"
import Box from "@mui/material/Box"

type DetailTab = {
  label: string
  content: React.ReactNode
  disabled?: boolean
}

type TabPanelProps = {
  children?: React.ReactNode
  index: number
  value: number
}

type DetailsTabsProps = {
  tabs: DetailTab[]
  ariaLabel?: string
}

function CustomTabPanel({ children, value, index, ...other }: TabPanelProps) {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`detail-tabpanel-${index}`}
      aria-labelledby={`detail-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ paddingInline: 0, paddingBlock: 4 }}>{children}</Box>}
    </div>
  )
}

function a11yProps(index: number) {
  return {
    id: `detail-tab-${index}`,
    "aria-controls": `detail-tabpanel-${index}`
  }
}

export default function DetailsTabs({ tabs, ariaLabel = "detail tabs" }: DetailsTabsProps) {
  const [value, setValue] = React.useState(0)

  const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue)
  }

  return (
    <Box sx={{ width: "100%" }}>
      <Box>
        <Tabs
          value={value}
          onChange={handleChange}
          textColor="secondary"
          indicatorColor="secondary"
          aria-label={ariaLabel}
        >
          {tabs.map((tab, index) => (
            <Tab
              key={tab.label}
              label={tab.label}
              disabled={tab.disabled}
              {...a11yProps(index)}
              sx={{ textTransform: "none" }}
            />
          ))}
        </Tabs>
      </Box>

      {tabs.map((tab, index) => (
        <CustomTabPanel key={tab.label} value={value} index={index}>
          {tab.content}
        </CustomTabPanel>
      ))}
    </Box>
  )
}
