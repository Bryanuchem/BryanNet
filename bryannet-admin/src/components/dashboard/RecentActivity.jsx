import {
    Avatar,
    Box,
    Divider,
    Skeleton,
    Stack,
    Typography,
} from "@mui/material";

import {
    Devices,
    Payments,
    PersonAdd,
    Wifi,
} from "@mui/icons-material";

import DashboardSection from "../common/DashboardSection";

import useRecentActivity from "../../hooks/useRecentActivity";

function getActivityIcon(type) {

    switch (type) {

        case "customer":
            return (
                <PersonAdd
                    color="primary"
                    fontSize="small"
                />
            );

        case "subscription":
            return (
                <Wifi
                    color="success"
                    fontSize="small"
                />
            );

        case "payment":
            return (
                <Payments
                    color="warning"
                    fontSize="small"
                />
            );

        case "device":
            return (
                <Devices
                    color="info"
                    fontSize="small"
                />
            );

        default:
            return (
                <PersonAdd
                    fontSize="small"
                />
            );

    }

}

function formatDate(date) {

    return new Date(date).toLocaleString(
        undefined,
        {
            dateStyle: "medium",
            timeStyle: "short",
        },
    );

}

function RecentActivity() {

    const {
        data = [],
        isLoading,
    } = useRecentActivity(5);

    return (

        <DashboardSection
            title="Recent Activity"
        >

            <Box
                sx={{
                    height: 420,
                    overflow: "hidden",
                    display: "flex",
                    flexDirection: "column",
                }}
            >

                {isLoading ? (

                    <Stack spacing={2}>

                        {[...Array(5)].map((_, index) => (

                            <Skeleton
                                key={index}
                                variant="rounded"
                                height={60}
                            />

                        ))}

                    </Stack>

                ) : data.length === 0 ? (

                    <Box
                        sx={{
                            flex: 1,
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                        }}
                    >

                        <Typography
                            color="text.secondary"
                        >
                            No recent activity.
                        </Typography>

                    </Box>

                ) : (

                    <Box
                        sx={{
                            flex: 1,
                            overflowY: "auto",
                            pr: 1,

                            "&::-webkit-scrollbar": {
                                width: 6,
                            },

                            "&::-webkit-scrollbar-thumb": {
                                bgcolor: "grey.400",
                                borderRadius: 10,
                            },

                            "&::-webkit-scrollbar-track": {
                                bgcolor: "transparent",
                            },
                        }}
                    >

                        <Stack
                            divider={<Divider />}
                        >

                            {data.map((activity, index) => (

                                <Box
                                    key={index}
                                    sx={{
                                        py: 2,
                                    }}
                                >

                                    <Stack
                                        direction="row"
                                        spacing={2}
                                        alignItems="flex-start"
                                    >

                                        <Avatar
                                            sx={{
                                                bgcolor: "grey.100",
                                                width: 42,
                                                height: 42,
                                            }}
                                        >

                                            {getActivityIcon(
                                                activity.type
                                            )}

                                        </Avatar>

                                        <Box
                                            sx={{
                                                flex: 1,
                                            }}
                                        >

                                            <Typography
                                                fontWeight={600}
                                            >
                                                {activity.title}
                                            </Typography>

                                            <Typography
                                                variant="body2"
                                                color="text.secondary"
                                                sx={{
                                                    mt: 0.5,
                                                }}
                                            >
                                                {activity.description}
                                            </Typography>

                                            <Typography
                                                variant="caption"
                                                color="text.secondary"
                                                sx={{
                                                    mt: 1,
                                                    display: "block",
                                                }}
                                            >
                                                {formatDate(
                                                    activity.created_at
                                                )}
                                            </Typography>

                                        </Box>

                                    </Stack>

                                </Box>

                            ))}

                        </Stack>

                    </Box>

                )}

            </Box>

        </DashboardSection>

    );

}

export default RecentActivity;