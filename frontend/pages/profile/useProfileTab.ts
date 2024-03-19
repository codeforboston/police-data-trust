import { useRouter } from "next/router"
import { useEffect, useState } from "react"
import { ProfileMenu } from "../../models/profile"

export function useProfileTab(initialTab: ProfileMenu) {
  const router = useRouter()
  const [activeTab, setActiveTab] = useState<ProfileMenu>(initialTab)

  useEffect(() => {
    const initialTab = router.query.tab as ProfileMenu
    if (Object.values(ProfileMenu).includes(initialTab)) {
      setActiveTab(initialTab)
    }

    const handleRouteChange = () => {
      const newTab = router.query.tab as ProfileMenu
      if (Object.values(ProfileMenu).includes(newTab)) {
        setActiveTab(newTab)
      }
    }

    router.events.on("routeChangeComplete", handleRouteChange)

    return () => {
      router.events.off("routeChangeComplete", handleRouteChange)
    }
  }, [router])

  const handleTabChange = (newTab: ProfileMenu) => {
    router.push(`?tab=${newTab}`)
  }

  return [activeTab, handleTabChange] as [ProfileMenu, (newTab: ProfileMenu) => void]
}
