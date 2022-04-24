import userEvent from "@testing-library/user-event"
import { geoAlbersUsa } from "d3-geo"
import { FeatureCollection } from "geojson"
import { after } from "lodash"
import * as React from "react"
import { act } from "react-test-renderer"
import { Map } from "../../compositions"
import BaseMap from "../../compositions/visualizations/map/BaseMap"
import { useBoundaryPaths } from "../../compositions/visualizations/map/useBoundaryPaths"
import { useAuth } from "../../helpers"
import { render, renderHook, setAuthForTest, waitFor } from "../test-utils"

describe("the map", () => {
  beforeAll(() => setAuthForTest())
  

//   const projection = geoAlbersUsa()
//     .scale(1300)
//     .translate([487.5 + 112, 305 + 50])

//   it("renders BaseMap correctly", async () => {
//     const {
//       result: { current: boundaryPaths }
//     } = renderHook(() => useBoundaryPaths())

//     const { result: {current: {user}} } = renderHook(() => useAuth())

//     console.log(user)

//     const { getByTestId } = render(
//       <BaseMap geoData={boundaryPaths} projection={projection} />
//     )

//     const yellowRect = getByTestId("yellow-rect")
//     const baseMap = getByTestId("basemapsvg")

//     act(() => userEvent.click(yellowRect))

//     await waitFor(() => expect(baseMap).resolves.toBeInTheDocument())

    
//   })

    it("renders Map correctly", async () => {
      const { container, findByTitle } = render(<Map />)
      await waitFor(() => expect(findByTitle("New York")).resolves.toBeInTheDocument())
    //   await new Promise(r => setTimeout(r, 1000))

      expect(container).toMatchSnapshot()
    })
})
