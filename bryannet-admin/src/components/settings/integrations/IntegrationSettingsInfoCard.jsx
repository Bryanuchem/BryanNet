import {
    Card,
    CardContent,
    Chip,
    Divider,
    Grid,
    Stack,
    Typography,
} from "@mui/material";

import HubIcon from "@mui/icons-material/Hub";

export default function IntegrationSettingsInfoCard({

    settings,

}) {

    const smtpConfigured =

        Boolean(

            settings.smtp_host &&

            settings.smtp_username &&

            settings.smtp_password,

        );

    const smsConfigured =

        Boolean(

            settings.sms_provider &&

            settings.sms_api_key,

        );

    return (

        <Card>

            <CardContent>

                <Stack spacing={3}>

                    <Stack

                        direction="row"

                        spacing={1}

                        alignItems="center"

                    >

                        <HubIcon

                            color="primary"

                        />

                        <Typography

                            variant="h6"

                        >

                            Integration Overview

                        </Typography>

                    </Stack>

                    <Typography

                        variant="body2"

                        color="text.secondary"

                    >

                        Review the current email and SMS integration services configured for the BryanNet ISP Platform.

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

                                    SMTP Host

                                </Typography>

                                <Typography>

                                    {

                                        settings.smtp_host ||

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

                                    SMTP Port

                                </Typography>

                                <Chip

                                    color="primary"

                                    label={

                                        settings.smtp_port ||

                                        "-"

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

                                    SMTP Security

                                </Typography>

                                <Chip

                                    color={

                                        settings.smtp_use_tls

                                            ? "success"

                                            : "default"

                                    }

                                    label={

                                        settings.smtp_use_tls

                                            ? "TLS Enabled"

                                            : "TLS Disabled"

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

                                    Email Integration

                                </Typography>

                                <Chip

                                    color={

                                        smtpConfigured

                                            ? "success"

                                            : "warning"

                                    }

                                    label={

                                        smtpConfigured

                                            ? "Configured"

                                            : "Not Configured"

                                    }

                                />

                            </Stack>

                        </Grid>

                    </Grid>

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

                                    SMS Provider

                                </Typography>

                                <Typography>

                                    {

                                        settings.sms_provider ||

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

                                    SMS Integration

                                </Typography>

                                <Chip

                                    color={

                                        smsConfigured

                                            ? "success"

                                            : "warning"

                                    }

                                    label={

                                        smsConfigured

                                            ? "Configured"

                                            : "Not Configured"

                                    }

                                />

                            </Stack>

                        </Grid>

                    </Grid>

                </Stack>

            </CardContent>

        </Card>

    );

}