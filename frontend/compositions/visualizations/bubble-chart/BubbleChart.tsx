import { extent } from "d3"
import React, { useEffect, useState } from "react"
import { CityProperties, Data } from "../../../models/visualizations"
import { DataPoint, formatSymbolData, parseProperties } from "../charts"
import useData from "../map/useData"
import styles from "./bubble.module.css"
import BubbleKey from "./bubbleKey"
import { Bubbles } from "./bubbles"

export default function BubbleChart() {
  const rawData: Data = useData()
  const [data, setData] = useState<CityProperties[]>([])
  const [shift, setShift] = useState(10)
  const [symbolProps, setSymbolProps] = useState<DataPoint[]>()
  const [filter, setFilter] = useState({
    property: "city",
    value: "all",
    sliceMin: 10,
    sliceMax: 30
  })
  const [sliceMax, setSliceMax] = useState(20)
  const [sliceMin, setSliceMin] = useState(10)

  useEffect(() => {
    if (!rawData) return
    console.log("rawData", rawData)
    rawData.setFilterProperties(filter)
    const cityProperties = rawData.features.map((f) => parseProperties(f) as CityProperties)
    setData(cityProperties)
  }, [filter, rawData])

  useEffect(() => {
    if (!data) return
    setSymbolProps(formatSymbolData(data, shift).sort((a, b) => (a.value - b.value ? 0 : 1)))
  }, [data, shift])

  return (
    <>
      <div style={{ display: "flex", flexDirection: "row", justifyContent: "center" }}>
        <div style={{ position: "relative" }}>
          {data ? <Bubbles data={symbolProps} /> : <div>waiting for data</div>}
          <div className={styles.inset}>
            <div className={styles.filterWrapper}>
              <input
                className={styles.filterInput}
                type={"text"}
                value={sliceMin}
                placeholder={sliceMin.toString()}
                id="sliceMin"
                onChange={(event) => setSliceMin(Number(event.target.value))}
              />
              <input
                className={styles.filterInput}
                type={"text"}
                value={sliceMax}
                placeholder={sliceMax.toString()}
                id="sliceMax"
                onChange={(event) => setSliceMax(Number(event.target.value))}
              />
              <button
                type="button"
                className="primaryButton"
                onClick={() => {
                  setFilter((filter) => {
                    return {
                      ...filter,
                      sliceMin: sliceMin,
                      sliceMax: sliceMax
                    }
                  })
                }}>
                Set Filter
              </button>
            </div>
            <div style={{ position: "relative" }}>
              <BubbleKey dataMaxMin={extent(data.map((d) => d.population))} />
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
