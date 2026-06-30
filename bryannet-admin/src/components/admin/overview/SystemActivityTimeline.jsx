import {
    Box,
    Divider,
    Paper,
    Stack,
    Typography,
} from "@mui/material";

export default function SystemActivityTimeline({
    activity = [],
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

    if (activity.length === 0) {
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
        <Paper variant="outlined">
            <Stack divider={<Divider />}>
                {activity.map((event) => (
                    <Box
                        key={event.id}
                        sx={{
                            display: "flex",
                            gap: 2,
                            p: 2,
                        }}
                    >
                        <Box
                            sx={{
                                width: 70,
                                flexShrink: 0,
                            }}
                        >
                            <Typography
                                variant="caption"
                                color="text.secondary"
                            >
                                {new Date(event.timestamp).toLocaleTimeString(
                                    [],
                                    {
                                        hour: "2-digit",
                                        minute: "2-digit",
                                    }
                                )}
                            </Typography>
                        </Box>

                        <Box
                            sx={{
                                width: 12,
                                display: "flex",
                                justifyContent: "center",
                            }}
                        >
                            <Box
                                sx={{
                                    width: 10,
                                    height: 10,
                                    mt: 0.8,
                                    borderRadius: "50%",
                                    bgcolor: "primary.main",
                                }}
                            />
                        </Box>

                        <Box sx={{ flexGrow: 1 }}>
                            <Typography
                                variant="subtitle2"
                                gutterBottom
                            >
                                {event.title}
                            </Typography>

                            <Typography
                                variant="body2"
                                color="text.secondary"
                            >
                                {event.description}
                            </Typography>
                        </Box>
                    </Box>
                ))}
            </Stack>
        </Paper>
    );
}