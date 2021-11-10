import {
  faAngleDoubleLeft,
  faAngleDoubleRight,
  faAngleLeft,
  faAngleRight,
  faEdit,
  IconDefinition
} from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import styles from "./data-table.module.css"

type EditButtonProps = {
  inEditMode: Boolean
  onclick: () => void
}

const EditButton = (props: EditButtonProps) => {
  const { editButtonOn, editButton } = styles
  const { inEditMode, onclick } = props

  return (
    <button
      className={inEditMode ? editButtonOn : editButton}
      title="Edit Result Filter"
      onClick={onclick}>
      <FontAwesomeIcon icon={faEdit} />
    </button>
  )
}

type PageButtonProps = {
  icon: IconDefinition
  onclick: () => void
  disabled?: boolean
}

const PageButton = (props: PageButtonProps) => {
  const { pageBtn } = styles
  const { icon, onclick, disabled } = props

  return (
    <button className={pageBtn} onClick={onclick} disabled={disabled}>
      <FontAwesomeIcon icon={icon} />
    </button>
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
      <span className={recordCount}>Found {data.length.toLocaleString()} records</span>
      <PageButton
        icon={faAngleDoubleLeft}
        onclick={() => gotoPage(0)}
        disabled={!canPreviousPage}
      />
      <PageButton icon={faAngleLeft} onclick={() => previousPage()} disabled={!canPreviousPage} />
      <span className={pageCnt}>
        Page <strong>{pageIndex + 1}</strong> of <strong>{pageOptions.length}</strong>{" "}
      </span>
      <PageButton icon={faAngleRight} onclick={() => nextPage()} disabled={!canNextPage} />
      <PageButton
        icon={faAngleDoubleRight}
        onclick={() => gotoPage(pageCount - 1)}
        disabled={!canNextPage}
      />
      <span className={goto}>
        Go to page:{" "}
        <input
          type="number"
          className={dataRowPage}
          defaultValue={pageIndex + 1}
          onChange={(e) => {
            const page = e.target.value ? Number(e.target.value) - 1 : 0
            gotoPage(page)
          }}
          style={{ width: "50px", textAlign: "right" }}
        />
      </span>{" "}
      <select value={pageSize} onChange={(e) => setPageSize(Number(e.target.value))}>
        {[10, 20, 30, 40, 50].map((pageSize) => (
          <option key={pageSize} value={pageSize}>
            Show {pageSize}
          </option>
        ))}
      </select>
    </div>
  )
}

export type { EditButtonProps, PageNavigatorProps }
export { EditButton, PageNavigator }
