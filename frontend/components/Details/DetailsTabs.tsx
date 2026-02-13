import * as React from "react"
import Tabs from "@mui/material/Tabs"
import Tab from "@mui/material/Tab"
import Box from "@mui/material/Box"
import { Typography } from "@mui/material"
import { Officer } from "@/utils/api"
import Employment from "./Employment"
import AllegationsSummary from "./AllegationsSummary"
import StateRecords from "./StateRecords"
import Lawsuits from "./Lawsuits"
import Awards from "./Awards"
import Attachments from "./Attachments"

interface TabPanelProps {
  children?: React.ReactNode
  index: number
  value: number
}

function CustomTabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ paddingInline: 0, paddingBlock: 4 }}>{children}</Box>}
    </div>
  )
}

function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    "aria-controls": `simple-tabpanel-${index}`
  }
}

export default function DetailsTabs(officer: Officer) {
  const [value, setValue] = React.useState(0)

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
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
          aria-label="detail tabs"
        >
          <Tab label="Background" {...a11yProps(0)} sx={{ textTransform: "none" }} />
          <Tab label="Complaints" {...a11yProps(1)} disabled sx={{ textTransform: "none" }} />
          <Tab label="Lawsuits" {...a11yProps(2)} disabled sx={{ textTransform: "none" }} />
          <Tab label="Awards" {...a11yProps(3)} disabled sx={{ textTransform: "none" }} />
          <Tab label="Attachments" {...a11yProps(4)} disabled sx={{ textTransform: "none" }} />
        </Tabs>
      </Box>
      <CustomTabPanel value={value} index={0}>
        <Typography component="h2" variant="h5" sx={{ fontSize: "1.3rem", fontWeight: "500" }}>
          Background
        </Typography>
        <StateRecords officer={officer} />
        <Employment employment_history={officer.employment_history} />
        <AllegationsSummary allegation_summary={officer.allegation_summary} />
        <Lawsuits />
        <Awards />
        <Attachments />
      </CustomTabPanel>
      <CustomTabPanel value={value} index={1}>
        Complaints
      </CustomTabPanel>
      <CustomTabPanel value={value} index={2}>
        Lawsuits
      </CustomTabPanel>
      <CustomTabPanel value={value} index={3}>
        Awards
      </CustomTabPanel>
      <CustomTabPanel value={value} index={4}>
        Attachments
      </CustomTabPanel>
    </Box>
  )
}
