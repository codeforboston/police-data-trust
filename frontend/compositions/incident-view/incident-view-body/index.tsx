import IncidentData from './incident-data'
import Map from './incident-google-map'
import { Incident } from '../../../helpers/incident'
import styles from './incident-body.module.css'

export default function IncidentBody(incident : Incident) {
    const { bodyWrapper, bodyElement } = styles
    return (
        <div className={bodyWrapper}>
            <Map />
            <IncidentData {...incident} />
        </div>
    )
}