import {
    Card,
    CardContent,
    Chip,
    Divider,
    Grid,
    Stack,
    Typography,
} from "@mui/material";

import NotificationsActiveIcon from "@mui/icons-material/NotificationsActive";

export default function NotificationSettingsInfoCard({

    settings,

}) {

    return (

        <Card>

            <CardContent>

                <Stack spacing={3}>

                    <Stack

                        direction="row"

                        spacing={1}

                        alignItems="center"

                    >

                        <NotificationsActiveIcon

                            color="primary"

                        />

                        <Typography

                            variant="h6"

                        >

                            Notification Overview

                        </Typography>

                    </Stack>

                    <Typography

                        variant="body2"

                        color="text.secondary"

                    >

                        Review how BryanNet communicates important billing, account and network updates to customers.

                    </Typography>

                    <Divider />

                    <Grid

                        container

                        spacing={3}

                    >

                        <Grid

                            size={{

                                xs: 12,

                                md: 6,

                            }}

                        >

                            <Stack spacing={1}>

                                <Typography

                                    variant="caption"

                                    color="text.secondary"

                                >

                                    Email Notifications

                                </Typography>

                                <Chip

                                    color={

                                        settings.email_notifications

                                            ? "success"

                                            : "default"

                                    }

                                    label={

                                        settings.email_notifications

                                            ? "Enabled"

                                            : "Disabled"

                                    }

                                />

                            </Stack>

                        </Grid>

                        <Grid

                            size={{

                                xs: 12,

                                md: 6,

                            }}

                        >

                            <Stack spacing={1}>

                                <Typography

                                    variant="caption"

                                    color="text.secondary"

                                >

                                    SMS Notifications

                                </Typography>

                                <Chip

                                    color={

                                        settings.sms_notifications

                                            ? "success"

                                            : "default"

                                    }

                                    label={

                                        settings.sms_notifications

                                            ? "Enabled"

                                            : "Disabled"

                                    }

                                />

                            </Stack>

                        </Grid>

                    </Grid>

                    <Divider />

                    <Stack spacing={2}>

                        <Typography

                            variant="subtitle2"

                        >

                            Automated Notifications

                        </Typography>

                        <Stack

                            direction="row"

                            spacing={1}

                            flexWrap="wrap"

                        >

                            <Chip

                                size="small"

                                color={

                                    settings.payment_reminders

                                        ? "success"

                                        : "default"

                                }

                                label="Payment Reminders"

                            />

                            <Chip

                                size="small"

                                color={

                                    settings.low_balance_alerts

                                        ? "success"

                                        : "default"

                                }

                                label="Low Balance Alerts"

                            />

                            <Chip

                                size="small"

                                color={

                                    settings.outage_alerts

                                        ? "success"

                                        : "default"

                                }

                                label="Outage Alerts"

                            />

                        </Stack>

                    </Stack>

                </Stack>

            </CardContent>

        </Card>

    );

}