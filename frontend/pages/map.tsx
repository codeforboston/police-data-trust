import dynamic from "next/dynamic"

// Temporary page to display the leaflet map for development

export default dynamic(() => import("../components/Map"), { ssr: false })