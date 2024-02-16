import { useEffect, useState } from "react"

let idCounter = 0

const useId = () => {
  const [id] = useState(() => `generated-id-${idCounter++}`)

  useEffect(() => {
    // Reset the counter when the component unmounts
    return () => {
      idCounter = 0
    }
  }, [])

  return id
}

export default useId
