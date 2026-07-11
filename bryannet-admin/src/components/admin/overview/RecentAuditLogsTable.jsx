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

export default function RecentAuditLogsTable({
    logs = [],
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
                    Loading audit logs...
                </Typography>

            </Paper>

        );

    }

    if (logs.length === 0) {

        return (

            <Paper
                variant="outlined"
                sx={{
                    p: 4,
                    textAlign: "center",
                }}
            >

                <Typography color="text.secondary">
                    No recent audit logs found.
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

                    {logs.map((log, index) => (

                        <TableRow

                            key={log.id}

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
                                    log.timestamp,
                                ).toLocaleTimeString(
                                    [],
                                    {

                                        hour: "2-digit",

                                        minute: "2-digit",

                                    },
                                )}

                            </TableCell>

                            <TableCell>

                                {log.administrator}

                            </TableCell>

                            <TableCell>

                                {log.action}

                            </TableCell>

                            <TableCell>

                                {log.module}

                            </TableCell>

                            <TableCell>

                                {log.target}

                            </TableCell>

                            <TableCell>

                                <BadgeChip

                                    status={
                                        log.status?.toLowerCase()
                                    }

                                    label={
                                        log.status
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