import { scaleLinear } from "d3"
import React from "react"
import { Circle, Square } from "../utilities"
import styles from "./chartKey.module.css"
import { steppedGradient } from "../utilities/chartScales"
import { GradientKeyItemProps, KeyItemProps, Position } from "../utilities/chartTypes"

export default function ChartKey(props: {
  title: string
  entries: JSX.Element[]
  position: Position
}) {
  const dirs = props.position.split(" ")
  const style: { [name: string]: string } = {}

  dirs.forEach((p) => (style[p] = "0"))

  return (
    <div id={`${props.title}`} className={styles.chartKeyContainer} style={style}>
      {React.Children.map(props.entries, (item, i) => (
        <KeyEntryWrapper key={i}>{item}</KeyEntryWrapper>
      ))}
    </div>
  )
}

export function KeyEntryWrapper(props: { children: React.ReactNode }) {
  return <div className={styles.KeyEntry}>{props.children}</div>
}

export function SymbolKeyItem(props: KeyItemProps) {
  const { label, symbol, color } = props
  return (
    <div className={styles.keySymbolEntry}>
      <KeySymbol color={color} symbol={symbol} />
      <label htmlFor={label} className={styles.label}>
        {label}
      </label>
    </div>
  )
}

export function GradientKeyItem(props: GradientKeyItemProps) {
  const { lowLabel, highLabel, colorTheme, colorScale, symbol, title } = props
  const colorSteps = steppedGradient(4, colorTheme, colorScale)

  return (
    <>
      <div>{title}</div>
      <div className={styles.keyGradientEntry}>
        <label className={styles.label}>{lowLabel}</label>
        {colorSteps.map((colorStep, i) => (
          <KeySymbol color={colorStep} symbol={symbol} key={i} />
        ))}
        <label className={styles.label}>{highLabel}</label>
      </div>
    </>
  )
}

export function scaleDataToColorTheme(lowValue: number, highValue: number) {
  return scaleLinear().domain([lowValue, highValue]).range([0, 1])
}

export function KeySymbol(props: { color: string; symbol: string }) {
  const { color, symbol } = props
  return symbol === "circle" ? (
    <Circle location={{ x: 20, y: 20 }} size={20} color={color} />
  ) : (
    <Square location={{ x: 20, y: 0 }} size={20} color={color} />
  )
}
