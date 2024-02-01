import React from 'react';
import styles from './side-menu.module.css';

interface SideMenu {
    
}

export default function SideMenu(){

  return (
    <div className={styles.sidebar}>
    
      <h2>Users</h2>
      <div className={styles.menu_space}></div>
      <h2>Incidents</h2>
      <div className={styles.menu_space}></div>
      <h2>Integrations</h2>
      <div className={styles.menu_space}></div>
      <h2> </h2>

    </div>
  );
};


