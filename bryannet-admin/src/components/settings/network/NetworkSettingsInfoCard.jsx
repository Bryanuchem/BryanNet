import {
    Card,
    CardContent,
    Chip,
    Divider,
    Grid,
    Stack,
    Typography,
} from "@mui/material";

import RouterIcon from "@mui/icons-material/Router";

export default function NetworkSettingsInfoCard({

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

                        <RouterIcon

                            color="primary"

                        />

                        <Typography

                            variant="h6"

                        >

                            Network Overview

                        </Typography>

                    </Stack>

                    <Typography

                        variant="body2"

                        color="text.secondary"

                    >

                        Review the default network configuration used throughout the BryanNet ISP Platform.

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

                                    Default Router

                                </Typography>

                                <Typography>

                                    {

                                        settings.default_router ||

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

                                    Bandwidth Unit

                                </Typography>

                                <Chip

                                    color="primary"

                                    label={

                                        settings.bandwidth_unit ||

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

                                    Primary DNS

                                </Typography>

                                <Typography>

                                    {

                                        settings.dns_primary ||

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

                                    Secondary DNS

                                </Typography>

                                <Typography>

                                    {

                                        settings.dns_secondary ||

                                        "-"

                                    }

                                </Typography>

                            </Stack>

                        </Grid>

                        <Grid

                            size={{

                                xs: 12,

                                md: 12,

                            }}

                        >

                            <Stack spacing={1}>

                                <Typography

                                    variant="caption"

                                    color="text.secondary"

                                >

                                    DHCP Lease Time

                                </Typography>

                                <Chip

                                    color="success"

                                    label={`${settings.dhcp_lease_time ?? 24} Hours`}

                                />

                            </Stack>

                        </Grid>

                    </Grid>

                </Stack>

            </CardContent>

        </Card>

    );

}