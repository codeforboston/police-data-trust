"use client"

import styles from "./updateCard.module.css"

type UpdateCardProps = {
  title: string
  updates: string[]
}

const UpdateCard = ({ title, updates }: UpdateCardProps) => {
  return (
    <div className={styles.card}>
      <h3 className={styles.cardTitle}>{title}</h3>
      <ul className={styles.updateList}>
        {updates.map((update, index) => (
          <li className={styles.cardItem} key={index}>
            {update}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default UpdateCard
