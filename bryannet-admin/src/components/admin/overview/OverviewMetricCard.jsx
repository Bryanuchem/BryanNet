import { Card, CardContent, Stack, Typography, Skeleton } from "@mui/material";

export default function OverviewMetricCard({
    title,
    value,
    subtitle = "",
    icon = null,
    loading = false,
}) {
    return (
        <Card elevation={1} sx={{ height: "100%" }}>
            <CardContent>
                <Stack spacing={2}>
                    <Stack
                        direction="row"
                        justifyContent="space-between"
                        alignItems="center"
                    >
                        <Typography
                            variant="body2"
                            color="text.secondary"
                        >
                            {title}
                        </Typography>

                        {icon}
                    </Stack>

                    {loading ? (
                        <Skeleton width={80} height={42} />
                    ) : (
                        <Typography variant="h4" fontWeight={700}>
                            {value}
                        </Typography>
                    )}

                    {loading ? (
                        <Skeleton width="60%" />
                    ) : (
                        <Typography
                            variant="body2"
                            color="text.secondary"
                        >
                            {subtitle}
                        </Typography>
                    )}
                </Stack>
            </CardContent>
        </Card>
    );
}