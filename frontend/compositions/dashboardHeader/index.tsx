import * as React from "react"
import { useMediaQuery } from './media-query-helper'
import LogoMobile from './assets/LogoMobile.svg'
// import NPDCLogo from './assets/NPDCLogo.svg'
import NPDCLogo from '../../shared-components/logo'
import HamburgerMenu from './assets/Vector.svg'
import DesktopNav from './desktopNav'
import styles from './dashboardHeader.module.css'

export default function DashboardHeader() : JSX.Element {
  const {
    wrapper,
    backgroundBanner,
    leftHeader,
    logo,
    mobileLogo,
    desktopLogo,
    titleContainer,
    mobileTitle,
    desktopTitle,
    rightHeader,
    nav,
    mobileNav,
    desktopNav,
    button,
  } = styles;

  // const belowBreakpoint = useMediaQuery(375);
  // const logo = belowBreakpoint ? <LogoMobile /> : <NPDCLogo />;
  // const title = belowBreakpoint ? 'N.P.D.C.' : 'National Police Data Coalition';
  // const navBar = belowBreakpoint ? <HamburgerMenu /> : <DesktopNav />

  return (
    <header className={wrapper}>
      <div className={backgroundBanner}>
        <div className={leftHeader}>
          {/* <div className={mobileLogo}> */}
            {/* {logo} */}
            {/* <LogoMobile />
          </div> */}
          <div className={logo}>
            {/* {logo} */}
            <NPDCLogo />
          </div>
          <div className={titleContainer}>
            {/* <h2>{title}</h2> */}
            <h2 className={mobileTitle}>N.P.D.C.</h2>
            <h2 className={desktopTitle}>National Police Data Coalition</h2>
            <p>The national index of police incidents</p>
          </div>
        </div>

        <div className={rightHeader}>
          <nav className={nav}>
            {/* {navBar} */}
            <div className={mobileNav}>
              <HamburgerMenu />
            </div>
            <div className={desktopNav}>
              <DesktopNav />
            </div>
          </nav>
          <button className={button} type="button">
            DONATE
          </button>
        </div>
      </div>
    </header>
  )
}
