import { Pagination } from "@mui/material"

type PaginationProps = {
  count?: number
  page?: number
  onChangeHandler?: (event: React.ChangeEvent<unknown>, value: number) => void
}

const PaginationComponent = ({ count = 10, page = 1, onChangeHandler }: PaginationProps) => {
  return (
    <Pagination
      count={count}
      page={page}
      onChange={onChangeHandler}
      color="primary"
      shape="rounded"
      sx={{
        display: "flex",
        justifyContent: "center",
        mt: 2,
        "& .MuiPaginationItem-root": {
          fontSize: "14px",
          minWidth: "32px",
          height: "32px"
        }
      }}
    />
  )
}

export default PaginationComponent
