import dynamic from 'next/dynamic'


const Map: any = dynamic(()=> import("../../compositions/map"), {ssr: false})

export default function Dashboard() {
  return (
    <div className="Dashboard">
      I AM DASHBORD!!!!!!
      <Map />
    </div>
  )
}
