import { GeoJson } from "../../../models/visualizations"
import { PointCoord } from "../utilities/chartTypes"

const emptyFakeData: GeoJson = { type: "FeatureCollection", features: [] }

type StateID = string

type FakeData = {
  UID: number
  location?: PointCoord
  state?: StateID
  label?: string
  value?: number
}

export default function useData() {
  // using temp dummy data set
  // const data = emptyFakeData

  const data: FakeData[] = [
    {
      UID: 1,
      state: "04",
      value: 10
    },
    {
      UID: 2,
      state: "05",
      value: 30
    },
    {
      UID: 3,
      state: "06",
      value: 100
    },
    {
      UID: 4,
      state: "09",
      value: 70
    },
    {
      UID: 5,
      state: "10",
      value: 20
    },
    {
      UID: 6,
      state: "11",
      value: 10
    },
    {
      UID: 7,
      state: "12",
      value: 30
    },
    {
      UID: 8,
      state: "13",
      value: 100
    },
    {
      UID: 9,
      state: "14",
      value: 70
    },
    {
      UID: 10,
      state: "15",
      value: 20
    }
  ]

  return data
}

// const [filterProperties, setFilterProperties] = useState<Filter>({
//   property: "state_name",
//   value: "",
//   sliceMin: 0,
//   sliceMax: 100
// })

// return useMemo(() => {
//   const { property, value, sliceMin, sliceMax } = filterProperties

//   let filteredFeatures: Feature[]
//   if (value === "") {
//     filteredFeatures = [] as Feature[]
//   } else if (value === "all") {
//     filteredFeatures = data.features
//   } else {
//     filteredFeatures = data.features.filter((d: Feature) => d.properties[property] === value)
//   }

//   const minimum = sliceMin || 0
//   const maximum =
//     sliceMax && sliceMax < filteredFeatures.length ? sliceMax : filteredFeatures.length
//   return {
//     features: filteredFeatures.slice(minimum, maximum),
//     filter: filterProperties,
//     setFilterProperties
//   }
// }, [data.features, filterProperties])
// }
