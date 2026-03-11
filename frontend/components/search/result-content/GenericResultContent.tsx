import { Box, Typography } from "@mui/material"
import { SearchResponse } from "@/utils/api"

type GenericResultContentProps = {
  result: SearchResponse
}

export default function GenericResultContent({
  result
}: GenericResultContentProps) {
  return (
    <Box>
      <Typography variant="h6" component="div">
        {result.title}
      </Typography>

      <Typography
        variant="body2"
        component="div"
        sx={{ fontWeight: "bold", color: "#000", mt: 0.5 }}
      >
        {result.subtitle}
      </Typography>

      {result.details && result.details.length > 0 && (
        <Box sx={{ mt: 2 }}>
          <Box component="span" sx={{ fontSize: "14px", color: "#454C54" }}>
            {result.details.join(", ")}
          </Box>
        </Box>
      )}
    </Box>
  )
}