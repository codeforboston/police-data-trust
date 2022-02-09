import { DashboardHeader } from "../compositions"
import "../styles/globals.css"
import Head from "next/head"
import { AppProps } from "next/app"
import { Providers } from "../helpers"
import { api } from "../helpers"

const title = "NPDC Index"
const description =
  "A national archive of police data collected by journalists, lawyers, and activists around the country."
const keywords =
  "police, policing, data, statistics, mapping, misconduct, incidents, violence, brutality, race, racism, united states, U.S.A., police unions, sheriff, militarization"
export const logoAlt = "A blue circular logo design reads 'National Police Data Coalition'"

export default function MyApp({ Component, pageProps }: AppProps) {
  api.useMockServiceWorker()

  return (
    <>
      <Head>
        <title>{title}</title>
        <meta name="description" content={description} />
        <meta name="keywords" content={keywords} />
        <meta property="og:title" content={title} />
        <meta property="og:description" content={description} />
        <meta property="og:type" content="website" />
        <meta property="og:image" content="/NPDCLogo.svg" />
        <meta property="og:image:type" content="image/svg" />
        <meta property="og:image:width" content="400" />
        <meta property="og:image:height" content="400" />
        <meta property="og:image:alt" content={logoAlt} />
      </Head>
      <Providers>
        <DashboardHeader />
        <Component {...pageProps} />
      </Providers>
    </>
  )
}
