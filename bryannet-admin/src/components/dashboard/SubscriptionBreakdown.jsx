import {
    Box,
    Grid,
    Skeleton,
    Stack,
    Typography,
} from "@mui/material";

import {
    Cell,
    Pie,
    PieChart,
    ResponsiveContainer,
    Tooltip,
} from "recharts";

import DashboardSection from "../common/DashboardSection";
import useSubscriptionBreakdown from "../../hooks/useSubscriptionBreakdown";

const COLORS = {
    Active: "#2e7d32",
    Queued: "#ed6c02",
    Expired: "#d32f2f",
    Cancelled: "#616161",
};

function SubscriptionBreakdown() {

    const {
        data = [],
        isLoading,
    } = useSubscriptionBreakdown();

    const totalSubscriptions = data.reduce(
        (sum, item) => sum + item.count,
        0,
    );

    return (

        <DashboardSection title="Subscription Breakdown">

            {isLoading ? (

                <Skeleton
                    variant="rounded"
                    height={320}
                />

            ) : totalSubscriptions === 0 ? (

                <Typography
                    align="center"
                    color="text.secondary"
                    sx={{ py: 14 }}
                >
                    No subscription data available.
                </Typography>

            ) : (

                <Grid
                    container
                    alignItems="center"
                    spacing={2}
                    sx={{
                        minHeight: 320,
                    }}
                >

                    {/* Chart */}

                    <Grid
                        size={{
                            xs: 12,
                            md: 8,
                        }}
                    >

                        <Box
                            sx={{
                                position: "relative",
                                height: 300,
                            }}
                        >

                            <ResponsiveContainer>

                                <PieChart>

                                    <Pie
                                        data={data}
                                        dataKey="count"
                                        nameKey="status"
                                        cx="50%"
                                        cy="50%"
                                        innerRadius={78}
                                        outerRadius={112}
                                        paddingAngle={3}
                                    >

                                        {data.map((entry) => (

                                            <Cell
                                                key={entry.status}
                                                fill={COLORS[entry.status]}
                                            />

                                        ))}

                                    </Pie>

                                    <Tooltip />

                                </PieChart>

                            </ResponsiveContainer>

                            <Box
                                sx={{
                                    position: "absolute",
                                    inset: 0,
                                    display: "flex",
                                    flexDirection: "column",
                                    justifyContent: "center",
                                    alignItems: "center",
                                    pointerEvents: "none",
                                }}
                            >

                                <Typography
                                    variant="h2"
                                    fontWeight={700}
                                    lineHeight={1}
                                >
                                    {totalSubscriptions}
                                </Typography>

                                <Typography
                                    variant="caption"
                                    color="text.secondary"
                                    sx={{
                                        mt: 1,
                                        fontWeight: 700,
                                        letterSpacing: 1,
                                    }}
                                >
                                    TOTAL
                                </Typography>

                                <Typography
                                    variant="caption"
                                    color="text.secondary"
                                    sx={{
                                        fontWeight: 700,
                                        letterSpacing: 1,
                                    }}
                                >
                                    SUBSCRIPTIONS
                                </Typography>

                            </Box>

                        </Box>

                    </Grid>

                    {/* Legend */}

                    <Grid
                        size={{
                            xs: 12,
                            md: 4,
                        }}
                    >

                        <Box
                            sx={{
                                height: 300,
                                display: "flex",
                                alignItems: "center",
                                justifyContent: "center",
                            }}
                        >

                            <Stack
                                spacing={3}
                                sx={{
                                    width: "100%",
                                    maxWidth: 220,
                                }}
                            >

                                {data.map((item) => (

                                    <Box
                                        key={item.status}
                                        sx={{
                                            display: "flex",
                                            alignItems: "center",
                                            justifyContent: "space-between",
                                            width: "100%",
                                        }}
                                    >

                                        <Box
                                            sx={{
                                                display: "flex",
                                                alignItems: "center",
                                                gap: 1.5,
                                                flex: 1,
                                                minWidth: 0,
                                            }}
                                        >

                                            <Box
                                                sx={{
                                                    width: 12,
                                                    height: 12,
                                                    borderRadius: "50%",
                                                    bgcolor: COLORS[item.status],
                                                    flexShrink: 0,
                                                }}
                                            />

                                            <Typography
                                                fontWeight={500}
                                                noWrap
                                            >
                                                {item.status}
                                            </Typography>

                                        </Box>

                                        <Typography
                                            variant="h6"
                                            fontWeight={700}
                                            sx={{
                                                minWidth: 24,
                                                textAlign: "right",
                                            }}
                                        >
                                            {item.count}
                                        </Typography>

                                    </Box>

                                ))}

                            </Stack>

                        </Box>

                    </Grid>

                </Grid>

            )}

        </DashboardSection>

    );

}

export default SubscriptionBreakdown;