import {
    Card,
    CardContent,
    Chip,
    Divider,
    Grid,
    Stack,
    Typography,
} from "@mui/material";

import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";

export default function GeneralSettingsInfoCard({

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

                        <InfoOutlinedIcon

                            color="primary"

                        />

                        <Typography

                            variant="h6"

                        >

                            General Information

                        </Typography>

                    </Stack>

                    <Typography

                        variant="body2"

                        color="text.secondary"

                    >

                        These settings define the core identity of your BryanNet ISP Platform and are displayed throughout the administration portal.

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

                                    Platform Name

                                </Typography>

                                <Chip

                                    color="primary"

                                    label={

                                        settings.platform_name ||

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

                                    Company Name

                                </Typography>

                                <Chip

                                    label={

                                        settings.company_name ||

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

                                    Company Email

                                </Typography>

                                <Typography>

                                    {

                                        settings.company_email ||

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

                                    Company Phone

                                </Typography>

                                <Typography>

                                    {

                                        settings.company_phone ||

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

                                    Time Zone

                                </Typography>

                                <Typography>

                                    {

                                        settings.default_timezone ||

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

                                    Date Format

                                </Typography>

                                <Typography>

                                    {

                                        settings.date_format ||

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

                                    Currency

                                </Typography>

                                <Typography>

                                    {

                                        settings.default_currency ||

                                        "-"

                                    }

                                </Typography>

                            </Stack>

                        </Grid>

                    </Grid>

                </Stack>

            </CardContent>

        </Card>

    );

}