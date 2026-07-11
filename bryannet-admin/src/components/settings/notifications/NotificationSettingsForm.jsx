import {
    Card,
    CardContent,
    Divider,
    FormControlLabel,
    Grid,
    Stack,
    Switch,
    Typography,
} from "@mui/material";

export default function NotificationSettingsForm({

    settings,

    onChange,

    disabled = false,

}) {

    function handleSwitchChange(

        event,

    ) {

        const {

            name,

            checked,

        } = event.target;

        onChange(

            name,

            checked,

        );

    }

    return (

        <Card>

            <CardContent>

                <Stack spacing={4}>

                    <Stack spacing={1}>

                        <Typography variant="h6">

                            Notification Settings

                        </Typography>

                        <Typography

                            variant="body2"

                            color="text.secondary"

                        >

                            Configure how BryanNet sends automated notifications to customers.

                        </Typography>

                    </Stack>

                    <Divider />

                    <Stack spacing={3}>

                        <Typography

                            variant="subtitle1"

                        >

                            General Notifications

                        </Typography>

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

                                    <FormControlLabel

                                        control={

                                            <Switch

                                                name="email_notifications"

                                                checked={

                                                    settings.email_notifications ??

                                                    true

                                                }

                                                onChange={

                                                    handleSwitchChange

                                                }

                                                disabled={

                                                    disabled

                                                }

                                            />

                                        }

                                        label="Email Notifications"

                                    />

                                    <Typography

                                        variant="body2"

                                        color="text.secondary"

                                    >

                                        Send platform notifications through email.

                                    </Typography>

                                </Stack>

                            </Grid>

                            <Grid

                                size={{

                                    xs: 12,

                                    md: 6,

                                }}

                            >

                                <Stack spacing={1}>

                                    <FormControlLabel

                                        control={

                                            <Switch

                                                name="sms_notifications"

                                                checked={

                                                    settings.sms_notifications ??

                                                    false

                                                }

                                                onChange={

                                                    handleSwitchChange

                                                }

                                                disabled={

                                                    disabled

                                                }

                                            />

                                        }

                                        label="SMS Notifications"

                                    />

                                    <Typography

                                        variant="body2"

                                        color="text.secondary"

                                    >

                                        Send important alerts via SMS.

                                    </Typography>

                                </Stack>

                            </Grid>

                        </Grid>

                    </Stack>

                    <Divider />

                    <Stack spacing={3}>

                        <Typography

                            variant="subtitle1"

                        >

                            Customer Notifications

                        </Typography>

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

                                    <FormControlLabel

                                        control={

                                            <Switch

                                                name="payment_reminders"

                                                checked={

                                                    settings.payment_reminders ??

                                                    true

                                                }

                                                onChange={

                                                    handleSwitchChange

                                                }

                                                disabled={

                                                    disabled

                                                }

                                            />

                                        }

                                        label="Payment Reminders"

                                    />

                                    <Typography

                                        variant="body2"

                                        color="text.secondary"

                                    >

                                        Automatically remind customers before invoices become due.

                                    </Typography>

                                </Stack>

                            </Grid>

                            <Grid

                                size={{

                                    xs: 12,

                                    md: 6,

                                }}

                            >

                                <Stack spacing={1}>

                                    <FormControlLabel

                                        control={

                                            <Switch

                                                name="low_balance_alerts"

                                                checked={

                                                    settings.low_balance_alerts ??

                                                    true

                                                }

                                                onChange={

                                                    handleSwitchChange

                                                }

                                                disabled={

                                                    disabled

                                                }

                                            />

                                        }

                                        label="Low Balance Alerts"

                                    />

                                    <Typography

                                        variant="body2"

                                        color="text.secondary"

                                    >

                                        Notify customers when their account balance falls below the configured threshold.

                                    </Typography>

                                </Stack>

                            </Grid>

                        </Grid>

                    </Stack>

                    <Divider />

                    <Stack spacing={3}>

                        <Typography

                            variant="subtitle1"

                        >

                            Network Notifications

                        </Typography>

                        <Grid

                            container

                            spacing={3}

                        >

                            <Grid

                                size={{

                                    xs: 12,

                                }}

                            >

                                <Stack spacing={1}>

                                    <FormControlLabel

                                        control={

                                            <Switch

                                                name="outage_alerts"

                                                checked={

                                                    settings.outage_alerts ??

                                                    true

                                                }

                                                onChange={

                                                    handleSwitchChange

                                                }

                                                disabled={

                                                    disabled

                                                }

                                            />

                                        }

                                        label="Outage Alerts"

                                    />

                                    <Typography

                                        variant="body2"

                                        color="text.secondary"

                                    >

                                        Notify customers whenever planned maintenance or unexpected outages occur.

                                    </Typography>

                                </Stack>

                            </Grid>

                        </Grid>

                    </Stack>

                </Stack>

            </CardContent>

        </Card>

    );

}