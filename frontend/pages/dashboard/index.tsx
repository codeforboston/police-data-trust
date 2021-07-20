import dynamic from 'next/dynamic'
// import Map from "../../compositions/map"


const Map: any = dynamic(()=> import("../../compositions/map"), {ssr: false})

export default function Dashboard() {
  return (
    <div className="Dashboard">
      I AM DASHBORD!!!!!!
      <Map />
    </div>
  )
}
