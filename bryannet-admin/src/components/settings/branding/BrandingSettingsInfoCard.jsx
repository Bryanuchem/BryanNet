import {
    Box,
    Card,
    CardContent,
    Chip,
    Divider,
    Grid,
    Stack,
    Typography,
} from "@mui/material";

import PaletteIcon from "@mui/icons-material/Palette";

export default function BrandingSettingsInfoCard({

    settings,

}) {

    const logoConfigured = Boolean(

        settings.logo_url,

    );

    const faviconConfigured = Boolean(

        settings.favicon_url,

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

                        <PaletteIcon

                            color="primary"

                        />

                        <Typography

                            variant="h6"

                        >

                            Branding Overview

                        </Typography>

                    </Stack>

                    <Typography

                        variant="body2"

                        color="text.secondary"

                    >

                        Review the visual identity currently configured for the BryanNet ISP Platform.

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

                                    Primary Color

                                </Typography>

                                <Stack

                                    direction="row"

                                    spacing={1.5}

                                    alignItems="center"

                                >

                                    <Box

                                        sx={{

                                            width: 20,

                                            height: 20,

                                            borderRadius: 1,

                                            bgcolor:

                                                settings.primary_color ||

                                                "#1976d2",

                                            border: "1px solid",

                                            borderColor: "divider",

                                        }}

                                    />

                                    <Typography>

                                        {

                                            settings.primary_color ||

                                            "#1976d2"

                                        }

                                    </Typography>

                                </Stack>

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

                                    Secondary Color

                                </Typography>

                                <Stack

                                    direction="row"

                                    spacing={1.5}

                                    alignItems="center"

                                >

                                    <Box

                                        sx={{

                                            width: 20,

                                            height: 20,

                                            borderRadius: 1,

                                            bgcolor:

                                                settings.secondary_color ||

                                                "#424242",

                                            border: "1px solid",

                                            borderColor: "divider",

                                        }}

                                    />

                                    <Typography>

                                        {

                                            settings.secondary_color ||

                                            "#424242"

                                        }

                                    </Typography>

                                </Stack>

                            </Stack>

                        </Grid>

                    </Grid>

                    <Divider />

                    <Stack spacing={2}>

                        <Typography

                            variant="subtitle2"

                        >

                            Login Page

                        </Typography>

                        <Stack spacing={0.5}>

                            <Typography

                                variant="body1"

                                fontWeight={600}

                            >

                                {

                                    settings.login_page_title ||

                                    "Not Configured"

                                }

                            </Typography>

                            <Typography

                                variant="body2"

                                color="text.secondary"

                            >

                                {

                                    settings.login_page_subtitle ||

                                    "No subtitle configured."

                                }

                            </Typography>

                        </Stack>

                    </Stack>

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

                                    Logo

                                </Typography>

                                <Chip

                                    color={

                                        logoConfigured

                                            ? "success"

                                            : "default"

                                    }

                                    label={

                                        logoConfigured

                                            ? "Configured"

                                            : "Not Configured"

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

                                    Favicon

                                </Typography>

                                <Chip

                                    color={

                                        faviconConfigured

                                            ? "success"

                                            : "default"

                                    }

                                    label={

                                        faviconConfigured

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