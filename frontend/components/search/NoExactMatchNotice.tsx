import { Box, Divider, Typography } from "@mui/material"

type NoExactMatchNoticeProps = {
  message: string
}

/**
 * Sits above a list of partial matches when nothing matched the search exactly: the
 * message, centered, then a full-width line separating it from the list.
 */
export default function NoExactMatchNotice({ message }: NoExactMatchNoticeProps) {
  return (
    <Box sx={{ mb: 3 }}>
      <Typography role="status" sx={{ textAlign: "center" }}>
        {message}
      </Typography>
      <Divider sx={{ mt: 3, borderColor: "black" }} />
    </Box>
  )
}
