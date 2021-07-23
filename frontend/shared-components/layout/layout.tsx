import React from "react"
import styles from "./layout.module.css"

type Props = {
  children?: JSX.Element | JSX.Element[]
}
export default function Layout({ children }: Props) {
  const { Layout } = styles

  return <div className={Layout}>{children}</div>
}
