import { SearchResponse } from "@/utils/api"

export default function getResultHref(result: SearchResponse): string {
  switch (result.content_type) {
    case "Officer":
      return `/officer/${result.uid}`
    case "Agency":
      return `/agency/${result.uid}`
    case "Unit":
      return `/unit/${result.uid}`
    case "Complaint":
      return `/complaint/${result.uid}`
    case "Litigation":
      return `/litigation/${result.uid}`
    default:
      return "#"
  }
}