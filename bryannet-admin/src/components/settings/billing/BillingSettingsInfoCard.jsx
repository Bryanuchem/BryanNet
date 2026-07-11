import {
    Card,
    CardContent,
    Chip,
    Divider,
    Grid,
    Stack,
    Typography,
} from "@mui/material";

import PaymentsIcon from "@mui/icons-material/Payments";

export default function BillingSettingsInfoCard({

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

                        <PaymentsIcon

                            color="primary"

                        />

                        <Typography

                            variant="h6"

                        >

                            Billing Overview

                        </Typography>

                    </Stack>

                    <Typography

                        variant="body2"

                        color="text.secondary"

                    >

                        Review the default billing configuration, payment preferences and invoice policies for the BryanNet ISP Platform.

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

                                    Default Payment Method

                                </Typography>

                                <Typography>

                                    {

                                        settings.default_payment_method ||

                                        "-"

                                    }

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

                                <Typography

                                    variant="caption"

                                    color="text.secondary"

                                >

                                    Payment Channel

                                </Typography>

                                <Typography>

                                    {

                                        settings.default_payment_channel ||

                                        "-"

                                    }

                                </Typography>

                            </Stack>

                        </Grid>

                        <Grid

                            size={{

                                xs: 12,

                                md: 4,

                            }}

                        >

                            <Stack spacing={1}>

                                <Typography

                                    variant="caption"

                                    color="text.secondary"

                                >

                                    Invoice Due

                                </Typography>

                                <Chip

                                    color="primary"

                                    label={`${settings.invoice_due_days ?? 7} Days`}

                                />

                            </Stack>

                        </Grid>

                        <Grid

                            size={{

                                xs: 12,

                                md: 4,

                            }}

                        >

                            <Stack spacing={1}>

                                <Typography

                                    variant="caption"

                                    color="text.secondary"

                                >

                                    Suspend After

                                </Typography>

                                <Chip

                                    color="warning"

                                    label={`${settings.suspend_after_days ?? 30} Days`}

                                />

                            </Stack>

                        </Grid>

                        <Grid

                            size={{

                                xs: 12,

                                md: 4,

                            }}

                        >

                            <Stack spacing={1}>

                                <Typography

                                    variant="caption"

                                    color="text.secondary"

                                >

                                    Tax Rate

                                </Typography>

                                <Chip

                                    color="success"

                                    label={`${settings.tax_percentage ?? 0}%`}

                                />

                            </Stack>

                        </Grid>

                    </Grid>

                    <Divider />

                    <Stack spacing={2}>

                        <Typography

                            variant="subtitle2"

                        >

                            Billing Policy

                        </Typography>

                        <Chip

                            color={

                                settings.auto_suspend_overdue

                                    ? "success"

                                    : "default"

                            }

                            label={

                                settings.auto_suspend_overdue

                                    ? "Automatic Suspension Enabled"

                                    : "Automatic Suspension Disabled"

                            }

                            sx={{

                                width: "fit-content",

                            }}

                        />

                    </Stack>

                </Stack>

            </CardContent>

        </Card>

    );

}