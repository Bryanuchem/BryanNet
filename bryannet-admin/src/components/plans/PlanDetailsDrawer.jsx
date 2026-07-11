import {
    Box,
    Button,
    Card,
    CardContent,
    Divider,
    Drawer,
    Stack,
    Typography,
} from "@mui/material";

import SellIcon from "@mui/icons-material/Sell";
import PaymentsIcon from "@mui/icons-material/Payments";
import CalendarMonthIcon from "@mui/icons-material/CalendarMonth";
import SpeedIcon from "@mui/icons-material/Speed";
import DevicesIcon from "@mui/icons-material/Devices";
import HubIcon from "@mui/icons-material/Hub";

import BadgeChip from "../common/BadgeChip";
import InfoField from "../common/InfoField";

function PlanDetailsDrawer({

    open,

    plan,

    onClose,

}) {

    if (!plan) {

        return null;

    }

    const formatCurrency = (value) => {

        return `₦${Number(value).toLocaleString()}`;

    };

    return (

        <Drawer
            anchor="right"
            open={open}
            onClose={onClose}
        >

            <Box
                sx={{
                    width: 450,
                    height: "100%",
                    bgcolor: "#F8FAFC",
                    display: "flex",
                    flexDirection: "column",
                }}
            >

                {/* Header */}

                <Box
                    sx={{
                        bgcolor: "primary.main",
                        color: "white",
                        p: 4,
                    }}
                >

                    <Typography
                        variant="overline"
                    >
                        Plan Details
                    </Typography>

                    <Typography
                        variant="h4"
                        fontWeight={700}
                    >
                        {plan.plan_name}
                    </Typography>

                    <Typography
                        sx={{
                            opacity: 0.85,
                        }}
                    >
                        Plan #{plan.plan_id}
                    </Typography>

                </Box>

                {/* Content */}

                <Box
                    sx={{
                        flex: 1,
                        overflowY: "auto",
                        p: 3,
                    }}
                >

                    <Card elevation={1}>

                        <CardContent>

                            <Typography
                                variant="subtitle2"
                                fontWeight={700}
                                gutterBottom
                            >
                                PLAN INFORMATION
                            </Typography>

                            <Divider
                                sx={{
                                    mb: 3,
                                }}
                            />

                            <Stack
                                spacing={3}
                            >

                                <InfoField
                                    icon={<SellIcon />}
                                    label="Plan Name"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >
                                        {plan.plan_name}
                                    </Typography>

                                </InfoField>

                                <InfoField
                                    icon={<PaymentsIcon />}
                                    label="Price"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >
                                        {formatCurrency(
                                            plan.price,
                                        )}
                                    </Typography>

                                </InfoField>

                                <InfoField
                                    icon={<CalendarMonthIcon />}
                                    label="Duration"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >
                                        {
                                            plan.duration_days
                                        }{" "}
                                        days
                                    </Typography>

                                </InfoField>

                                <InfoField
                                    icon={<SpeedIcon />}
                                    label="Speed Limit"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >
                                        {
                                            plan.speed_limit_mbps
                                        }{" "}
                                        Mbps
                                    </Typography>

                                </InfoField>

                                <InfoField
                                    icon={<DevicesIcon />}
                                    label="Maximum Devices"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >
                                        {
                                            plan.max_devices
                                        }
                                    </Typography>

                                </InfoField>

                                <InfoField
                                    icon={<HubIcon />}
                                    label="Concurrent Devices"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >
                                        {
                                            plan.concurrent_devices
                                        }
                                    </Typography>

                                </InfoField>

                                <InfoField
                                    icon={<SellIcon />}
                                    label="Status"
                                >

                                    <BadgeChip
                                        status={
                                            plan.is_active
                                                ? "active"
                                                : "inactive"
                                        }
                                    />

                                </InfoField>

                            </Stack>

                        </CardContent>

                    </Card>

                </Box>

                {/* Footer */}

                <Box
                    sx={{
                        p: 3,
                        bgcolor: "white",
                        borderTop:
                            "1px solid #E5E7EB",
                    }}
                >

                    <Button
                        fullWidth
                        variant="contained"
                        size="large"
                        onClick={onClose}
                    >
                        Close
                    </Button>

                </Box>

            </Box>

        </Drawer>

    );

}

export default PlanDetailsDrawer;