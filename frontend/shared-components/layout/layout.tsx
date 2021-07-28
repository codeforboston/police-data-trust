import React from "react"
import styles from "./layout.module.css"

type Props = {
  children?: React.ReactNode
}
export default function Layout({ children }: Props) {
  const { Layout } = styles

  return <div className={Layout}>{children}</div>
}
