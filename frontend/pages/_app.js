import "../styles/globals.css"
import Head from "next/head"

const title = "NPDC Index"
const description =
  "A national archive of police data collected by journalists, lawyers, and activists around the country."
const keywords =
  "police, policing, data, statistics, mapping, misconduct, incidents, violence, brutality, race, racism, united states, U.S.A., police unions, sheriff, militarization"
export const logoAlt = "A blue circular logo design reads 'National Police Data Coalition'"

export default function MyApp({ Component, pageProps }) {
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
      <Component {...pageProps} />
    </>
  )
}
