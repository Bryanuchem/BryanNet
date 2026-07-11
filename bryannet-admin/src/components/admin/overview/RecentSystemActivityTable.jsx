import {
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Typography,
} from "@mui/material";

import BadgeChip from "../../common/BadgeChip";

export default function RecentSystemActivityTable({

    activities = [],

    loading = false,

}) {

    if (loading) {

        return (

            <Paper
                variant="outlined"
                sx={{
                    p: 4,
                    textAlign: "center",
                }}
            >

                <Typography color="text.secondary">

                    Loading system activity...

                </Typography>

            </Paper>

        );

    }

    if (activities.length === 0) {

        return (

            <Paper
                variant="outlined"
                sx={{
                    p: 4,
                    textAlign: "center",
                }}
            >

                <Typography color="text.secondary">

                    No recent system activity.

                </Typography>

            </Paper>

        );

    }

    return (

        <TableContainer
            component={Paper}
            variant="outlined"
        >

            <Table>

                <TableHead>

                    <TableRow>

                        <TableCell>Time</TableCell>

                        <TableCell>Administrator</TableCell>

                        <TableCell>Action</TableCell>

                        <TableCell>Module</TableCell>

                        <TableCell>Target</TableCell>

                        <TableCell>Status</TableCell>

                    </TableRow>

                </TableHead>

                <TableBody>

                    {activities.map((activity, index) => (

                        <TableRow

                            key={activity.id}

                            hover

                            sx={{

                                cursor: "pointer",

                                backgroundColor:

                                    index % 2 === 0

                                        ? "action.hover"

                                        : "background.paper",

                            }}

                        >

                            <TableCell>

                                {new Date(

                                    activity.timestamp,

                                ).toLocaleTimeString(

                                    [],

                                    {

                                        hour: "2-digit",

                                        minute: "2-digit",

                                    },

                                )}

                            </TableCell>

                            <TableCell>

                                {activity.administrator}

                            </TableCell>

                            <TableCell>

                                {activity.action}

                            </TableCell>

                            <TableCell>

                                {activity.module}

                            </TableCell>

                            <TableCell>

                                {

                                    activity.target

                                    ||

                                    "-"

                                }

                            </TableCell>

                            <TableCell>

                                <BadgeChip

                                    status={

                                        activity.status?.toLowerCase()

                                    }

                                    label={

                                        activity.status

                                    }

                                />

                            </TableCell>

                        </TableRow>

                    ))}

                </TableBody>

            </Table>

        </TableContainer>

    );

}