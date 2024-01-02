import {
  faAngleLeft,
  faAngleRight,
  IconDefinition
} from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import styles from "./officer-incident-data-table.module.css"


type PageButtonProps = {
  icon: IconDefinition
  onclick: () => void
  disabled?: boolean
}

const PageButton = (props: PageButtonProps) => {
  const { pageBtn } = styles
  const { icon, onclick, disabled } = props

  return (
    <span className={pageBtn} onClick={onclick}>
      <FontAwesomeIcon icon={icon} />
    </span>
  )
}
type PageNavigatorProps = {
  data: any[]
  gotoPage(n: number): void
  previousPage(): void
  nextPage(): void
  pageIndex: number
  pageOptions: number[]
  pageCount: number
  canPreviousPage: boolean
  canNextPage: boolean
  pageSize: number
  setPageSize(n: number): void
}

const PageNavigator = (props: PageNavigatorProps) => {
  const { dataFooter, dataRowPage, recordCount, pageCnt, goto } = styles
  const {
    data,
    gotoPage,
    previousPage,
    nextPage,
    pageIndex,
    pageOptions,
    pageCount,
    canPreviousPage,
    canNextPage,
    pageSize,
    setPageSize
  } = props

  return (
    <div className={dataFooter}>
      <span className={recordCount}>Number of results: {data.length}</span>
      <span>
        <PageButton icon={faAngleLeft} onclick={() => previousPage()} disabled={!canPreviousPage} />
        <span className={pageCnt}>
          {pageIndex + 1} of {pageOptions.length}
        </span>
        <PageButton icon={faAngleRight} onclick={() => nextPage()} disabled={!canNextPage} />
      </span>
    </div>
  )
}

export type { PageNavigatorProps }
export {PageNavigator }
