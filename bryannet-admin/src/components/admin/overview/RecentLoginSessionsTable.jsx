import {
    Chip,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Typography,
} from "@mui/material";

export default function RecentLoginSessionsTable({
    sessions = [],
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
                    Loading recent login sessions...
                </Typography>

            </Paper>

        );

    }

    if (sessions.length === 0) {

        return (

            <Paper
                variant="outlined"
                sx={{
                    p: 4,
                    textAlign: "center",
                }}
            >

                <Typography color="text.secondary">
                    No recent login sessions found.
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

                        <TableCell>Administrator</TableCell>

                        <TableCell>Device</TableCell>

                        <TableCell>Browser</TableCell>

                        <TableCell>IP Address</TableCell>

                        <TableCell>Login Time</TableCell>

                        <TableCell>Status</TableCell>

                    </TableRow>

                </TableHead>

                <TableBody>

                    {sessions.map((session, index) => (

                        <TableRow

                            key={session.id}

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

                                {session.administrator}

                            </TableCell>

                            <TableCell>

                                {session.device}

                            </TableCell>

                            <TableCell>

                                {session.browser}

                            </TableCell>

                            <TableCell>

                                {session.ip_address}

                            </TableCell>

                            <TableCell>

                                {new Date(
                                    session.login_time,
                                ).toLocaleTimeString(
                                    [],
                                    {
                                        hour: "2-digit",
                                        minute: "2-digit",
                                    },
                                )}

                            </TableCell>

                            <TableCell>

                                <Chip

                                    label={session.status}

                                    color={
                                        session.status === "Active"

                                            ? "success"

                                            : "warning"
                                    }

                                    size="small"

                                />

                            </TableCell>

                        </TableRow>

                    ))}

                </TableBody>

            </Table>

        </TableContainer>

    );

}