import dynamic from "next/dynamic"

// d3 does not support server-side rendering, so only render the Map component
// in the browser.
export default dynamic(() => import("./Map"), { ssr: false })
