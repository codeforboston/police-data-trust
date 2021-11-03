import { ResultsAlert } from "../../shared-components"
import { render } from "../test-utils"
import { SearchResultsTypes } from "../../models"

it("renders no results alert correctly", () => {
  const { container } = render(
    <ResultsAlert type={SearchResultsTypes.NORESULTS} returnHandler={() => {}} />
  )
  expect(container).toMatchSnapshot()
})

it("renders no search params alert correctly", () => {
  const { container } = render(
    <ResultsAlert type={SearchResultsTypes.NOSEARCHPARAMS} returnHandler={() => {}} />
  )
  expect(container).toMatchSnapshot()
})
