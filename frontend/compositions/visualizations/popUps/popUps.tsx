import { useCallback, useEffect, useMemo, useRef, useState } from "react"
import { Coord } from "../utilities/chartTypes"
import { PopUpProps } from "./popUpComp"

export type InteractionState<T> = {
  hovered: boolean
  shouldShowPopUp?: boolean
  headerText?: string
  bodyText?: string
  location?: Coord
}

const rootState: InteractionState<any> = {
  hovered: false,
  shouldShowPopUp: false,
  headerText: null,
  bodyText: null,
  location: null
}

export function usePopUp() {
  const [interactionState, setInteractionState] = useState<InteractionState<any>>(rootState)

  const popUpDuration = useRef(null)
  const popUpAppearDelay = useRef(null)

  const updatePopUp = useCallback(
    (newState: InteractionState<any>) => {
      clearTimeout(popUpAppearDelay.current)
      clearTimeout(popUpDuration.current)

      setInteractionState((prevState) => {
        return { ...prevState, hovered: newState.hovered, shouldShowPopUp: false }
      })

      popUpAppearDelay.current = setTimeout(() => {
        if (newState.headerText === undefined) return
        setInteractionState((prevState) => {
          return { ...prevState, ...newState, shouldShowPopUp: interactionState.hovered }
        })
      }, 800)

      popUpDuration.current = setTimeout(() => {
        setInteractionState((prevState) => {
          return { ...prevState, hovered: false, shouldShowPopUp: false }
        })
      }, 3000)
    },
    [interactionState.hovered]
  )

  const popUpProps: PopUpProps = useMemo(
    () => ({
      shouldShowPopUp: interactionState?.shouldShowPopUp,
      bodyText: interactionState?.bodyText,
      headerText: interactionState?.headerText,
      location: interactionState?.location
    }),
    [
      interactionState?.bodyText,
      interactionState?.headerText,
      interactionState?.location,
      interactionState?.shouldShowPopUp
    ]
  )
  return { popUpProps, updatePopUp }
}
