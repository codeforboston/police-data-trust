import { IncidentDetailType } from '../../../models'
import styles from './incident-view-header.module.css'

export default function IncidentViewHeader(incident: IncidentDetailType) {
    const { id, use_of_force, outcome } = incident
    const { idWrapper, detailWrapper, forceWrapper, outcomeWrapper, category } = styles
    const outcomeString = outcome.join(", ")
    function forcesToString(forces : typeof use_of_force) : string {
        const forceStrings : string[] = forces.map( (force) => {
            return force.item
        })
        return forceStrings.join(", ")
    }
    
    return (
        <div>
            <p className={idWrapper}>{id}</p>
            <div className={detailWrapper}>
                <p className={forceWrapper}>{forcesToString(use_of_force)}</p>
                <div className={outcomeWrapper}>
                    <p className={category}></p>
                    <p>{outcomeString}</p>
                </div>
            </div>
        </div>
    )
}