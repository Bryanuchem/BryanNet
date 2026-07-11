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

import PersonIcon from "@mui/icons-material/Person";
import SellIcon from "@mui/icons-material/Sell";
import CalendarTodayIcon from "@mui/icons-material/CalendarToday";
import EventBusyIcon from "@mui/icons-material/EventBusy";
import ScheduleIcon from "@mui/icons-material/Schedule";
import Avatar from "@mui/material/Avatar";

import BadgeChip from "../common/BadgeChip";
import InfoField from "../common/InfoField";

function SubscriptionDetailsDrawer({

    open,

    subscription,

    onClose,

}) {

    if (!subscription) {

        return null;

    }

    const formatDate = (date) => {

        if (!date) {

            return "-";

        }

        return new Date(
            date,
        ).toLocaleString();

    };

    const status =
        subscription.status?.toLowerCase();

    const startedLabel =
        status === "queued"
            ? "Starts"
            : status === "cancelled"
            ? "Would Have Started"
            : "Started";

    const expiryLabel =
        status === "expired"
            ? "Expired On"
            : status === "queued"
            ? "Will Expire"
            : status === "cancelled"
            ? "Would Have Expired"
            : "Expires";

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

                        display: "flex",

                        alignItems: "center",

                        gap: 3,

                    }}
                >

                    <Avatar
                        sx={{

                            width: 64,

                            height: 64,

                            bgcolor: "white",

                            color: "primary.main",

                            fontSize: 32,

                            fontWeight: 700,

                        }}
                    >

                        {subscription.customer_name?.[0] ?? "?"}

                    </Avatar>

                    <Box>

                        <Typography
                            variant="overline"
                        >

                            SUBSCRIPTION DETAILS

                        </Typography>

                        <Typography
                            variant="h4"
                            fontWeight={700}
                        >

                            {subscription.customer_name}

                        </Typography>

                        <Typography
                            sx={{

                                opacity: 0.9,

                            }}
                        >

                            {subscription.plan_name}

                        </Typography>

                    </Box>

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

                                SUBSCRIPTION INFORMATION

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
                                    icon={<PersonIcon />}
                                    label="Customer"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >

                                        {
                                            subscription.customer_name
                                        }

                                    </Typography>

                                </InfoField>

                                <InfoField
                                    icon={<SellIcon />}
                                    label="Plan"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >

                                        {
                                            subscription.plan_name
                                        }

                                    </Typography>

                                </InfoField>

                                <InfoField
                                    icon={<SellIcon />}
                                    label="Status"
                                >

                                    <BadgeChip

                                        status={

                                            subscription.status?.toLowerCase()

                                        }

                                        label={
                                            subscription.status
                                        }

                                    />

                                </InfoField>

                                <InfoField
                                    icon={<ScheduleIcon />}
                                    label="Remaining Days"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >

                                        {

                                            subscription.remaining_days

                                        }{" "}

                                        days

                                    </Typography>

                                </InfoField>

                                <InfoField
                                    icon={<CalendarTodayIcon />}
                                    label={startedLabel}
                                >

                                    <Typography
                                        fontWeight={500}
                                    >

                                        {

                                            formatDate(

                                                subscription.start_date,

                                            )

                                        }

                                    </Typography>

                                </InfoField>

                                <InfoField
                                    icon={<EventBusyIcon />}
                                    label={expiryLabel}
                                >

                                    <Typography
                                        fontWeight={500}
                                    >

                                        {

                                            formatDate(

                                                subscription.expiry_date,

                                            )

                                        }

                                    </Typography>

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

export default SubscriptionDetailsDrawer;