import * as React from 'react';

import { useTable } from "react-table"

type IncidentData = {
    dates: string;
    incidentType: string;
    officersInvolved: string[];
    subject: string;
    source: string;
}

// Defines table rows
// useMemo is being used here to 
const data = React.useMemo(
    () => [
        {
            dates: "2003/01/01",
            incidentType: "Use of force",
            officersInvolved: ["John Smith"],
            subject: "unknown",
            source: "News Article",
        },
        {
            dates: "2003/01/01",
            incidentType: "Use of force",
            officersInvolved: ["John Smith"],
            subject: "unknown",
            source: "News Article",
        },
        {
            dates: "2003/01/01",
            incidentType: "Use of force",
            officersInvolved: ["John Smith"],
            subject: "unknown",
            source: "News Article",
        },
        {
            dates: "2003/01/01",
            incidentType: "Use of force",
            officersInvolved: ["John Smith"],
            subject: "unknown",
            source: "News Article",
        },
        {
            dates: "2003/01/01",
            incidentType: "Use of force",
            officersInvolved: ["John Smith"],
            subject: "unknown",
            source: "News Article",
        },
        {
            dates: "2003/01/01",
            incidentType: "Use of force",
            officersInvolved: ["John Smith"],
            subject: "unknown",
            source: "News Article",
        },
        {
            dates: "2003/01/01",
            incidentType: "Use of force",
            officersInvolved: ["John Smith"],
            subject: "unknown",
            source: "News Article",
        },
    ],
    []
);

const columns = React.useMemo(
    () => [
        {
            Header: "Date(s)",
            accessor: "dates" as const,
        },
        {
            Header: "Incident Type",
            accessor: "incidentType" as const,
        },
        {
            Header: "Officer(s) Involved",
            accessor: "officersInvolved" as const,
        },
        {
            Header: "Subject",
            accessor: "subject" as const,
        },
        {
            Header: "Source",
            accessor: "source" as const,
        },
    ],
    []
);

function DataTable() {

    const tableInstance = useTable({ columns, data });

    return (
        <table>
            <thead>
                <tr>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td></td>
                </tr>
            </tbody>
        </table>
    );

}
