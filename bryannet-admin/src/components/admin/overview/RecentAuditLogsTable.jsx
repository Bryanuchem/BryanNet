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
        <TableContainer component={Paper} variant="outlined">
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
                    {logs.map((log) => (
                        <TableRow key={log.id} hover>
                            <TableCell>
                                {new Date(log.timestamp).toLocaleTimeString([], {
                                    hour: "2-digit",
                                    minute: "2-digit",
                                })}
                            </TableCell>

                            <TableCell>{log.administrator}</TableCell>

                            <TableCell>{log.action}</TableCell>

                            <TableCell>{log.module}</TableCell>

                            <TableCell>{log.target}</TableCell>

                            <TableCell>
                                <Chip
                                    label={log.status}
                                    color={
                                        log.status === "Success"
                                            ? "success"
                                            : "error"
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