import { scaleLinear } from "d3"
import React from "react"
import { Circle, Square } from "./"
import styles from "./chart.module.css"
import { steppedGradient } from "./chartScales"
import {
  GradientKeyItemProps, KeyItemProps, Position
} from "./chartTypes"
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
  const { lowLabel, highLabel, colorTheme, colorScale, symbol } = props
  const colorSteps = steppedGradient(4, colorTheme, colorScale)

  return (
    <div className={styles.keyGradientEntry}>
      <label className={styles.label}>{lowLabel}</label>
      {colorSteps.map((colorStep, i) => (
        <KeySymbol color={colorStep} symbol={symbol} key={i} />
      ))}
      <label className={styles.label}>{highLabel}</label>
    </div>
  )
}

export function KeyEntryWrapper(props: { children: React.ReactElement }) {
  return <div className={styles.KeyEntry}>{props.children}</div>
}

export default function ChartKey(props: {
  title: string
  children: React.ReactElement[]
  position: Position
}) {
  return (
    <div id="chart legend" className={styles.chartKeyContainer}>
      {React.Children.map(props.children, (item, i) => (
        <KeyEntryWrapper key={i} children={item} />
      ))}
    </div>
  )
}
