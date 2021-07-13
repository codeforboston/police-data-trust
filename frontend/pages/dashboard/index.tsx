import DashboardHeader from '../../compositions/dashboardHeader/index';
import styles  from '../../compositions/dashboardHeader/header.module.css';


export default function Dashboard() {

  const {
    backgroundBanner,
  } = styles;

  return <div className="Dashboard">
    <div className={backgroundBanner}></div>
    <DashboardHeader />
  </div>
}
