import * as d3 from "d3"




export function getCenter(el: Element): [number, number] {
  const { x, y, width, height } = el.getBoundingClientRect()

  return [(x + width) / 2, (y + height) / 2]
}

export function getDisplacementFromViewportCenter(el: Element) {
  const svg = document.querySelector("#show-data")
  const elementCenter = getCenter(el)
  const viewportCenter = getCenter(svg)
  console.log(elementCenter, viewportCenter)

  return [(elementCenter[0] + viewportCenter[0]) / 2, (elementCenter[1] - viewportCenter[1]) / 2]
}

export function getExtent(el: Element) {
  const { left, top, right, bottom } = el.getBoundingClientRect()
  return [
    [left, top],
    [right, bottom],
  ] as [[number, number], [number, number]]
}
