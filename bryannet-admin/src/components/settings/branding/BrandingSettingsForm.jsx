import {
    Box,
    Card,
    CardContent,
    Divider,
    Grid,
    Stack,
    TextField,
    Typography,
} from "@mui/material";

export default function BrandingSettingsForm({

    settings,

    onChange,

    disabled = false,

}) {

    function handleChange(

        event,

    ) {

        const {

            name,

            value,

        } = event.target;

        onChange(

            name,

            value,

        );

    }

    return (

        <Card>

            <CardContent>

                <Stack spacing={4}>

                    <Stack spacing={1}>

                        <Typography variant="h6">

                            Branding Settings

                        </Typography>

                        <Typography

                            variant="body2"

                            color="text.secondary"

                        >

                            Configure your organization's branding, colours and login page appearance.

                        </Typography>

                    </Stack>

                    <Divider />

                    <Stack spacing={3}>

                        <Typography

                            variant="subtitle1"

                        >

                            Visual Identity

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

                                <TextField

                                    fullWidth

                                    label="Logo URL"

                                    name="logo_url"

                                    value={

                                        settings.logo_url ??

                                        ""

                                    }

                                    onChange={

                                        handleChange

                                    }

                                    disabled={

                                        disabled

                                    }

                                    helperText="Public URL to the company logo."

                                />

                            </Grid>

                            <Grid

                                size={{

                                    xs: 12,

                                    md: 6,

                                }}

                            >

                                <TextField

                                    fullWidth

                                    label="Favicon URL"

                                    name="favicon_url"

                                    value={

                                        settings.favicon_url ??

                                        ""

                                    }

                                    onChange={

                                        handleChange

                                    }

                                    disabled={

                                        disabled

                                    }

                                    helperText="Public URL to the website favicon."

                                />

                            </Grid>

                        </Grid>

                    </Stack>

                    <Divider />

                    <Stack spacing={3}>

                        <Typography

                            variant="subtitle1"

                        >

                            Brand Colours

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

                                <Stack spacing={1.5}>

                                    <TextField

                                        fullWidth

                                        label="Primary Colour"

                                        name="primary_color"

                                        value={

                                            settings.primary_color ??

                                            "#1976d2"

                                        }

                                        onChange={

                                            handleChange

                                        }

                                        disabled={

                                            disabled

                                        }

                                    />

                                    <Box

                                        sx={{

                                            display: "flex",

                                            alignItems: "center",

                                            gap: 2,

                                        }}

                                    >

                                        <TextField

                                            type="color"

                                            name="primary_color"

                                            value={

                                                settings.primary_color ??

                                                "#1976d2"

                                            }

                                            onChange={

                                                handleChange

                                            }

                                            disabled={

                                                disabled

                                            }

                                            sx={{

                                                width: 90,

                                            }}

                                        />

                                        <Typography

                                            variant="body2"

                                            color="text.secondary"

                                        >

                                            Primary application colour

                                        </Typography>

                                    </Box>

                                </Stack>

                            </Grid>

                            <Grid

                                size={{

                                    xs: 12,

                                    md: 6,

                                }}

                            >

                                <Stack spacing={1.5}>

                                    <TextField

                                        fullWidth

                                        label="Secondary Colour"

                                        name="secondary_color"

                                        value={

                                            settings.secondary_color ??

                                            "#424242"

                                        }

                                        onChange={

                                            handleChange

                                        }

                                        disabled={

                                            disabled

                                        }

                                    />

                                    <Box

                                        sx={{

                                            display: "flex",

                                            alignItems: "center",

                                            gap: 2,

                                        }}

                                    >

                                        <TextField

                                            type="color"

                                            name="secondary_color"

                                            value={

                                                settings.secondary_color ??

                                                "#424242"

                                            }

                                            onChange={

                                                handleChange

                                            }

                                            disabled={

                                                disabled

                                            }

                                            sx={{

                                                width: 90,

                                            }}

                                        />

                                        <Typography

                                            variant="body2"

                                            color="text.secondary"

                                        >

                                            Secondary application colour

                                        </Typography>

                                    </Box>

                                </Stack>

                            </Grid>

                        </Grid>

                    </Stack>

                    <Divider />

                    <Stack spacing={3}>

                        <Typography

                            variant="subtitle1"

                        >

                            Login Page

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

                                <TextField

                                    fullWidth

                                    label="Login Page Title"

                                    name="login_page_title"

                                    value={

                                        settings.login_page_title ??

                                        ""

                                    }

                                    onChange={

                                        handleChange

                                    }

                                    disabled={

                                        disabled

                                    }

                                />

                            </Grid>

                            <Grid

                                size={{

                                    xs: 12,

                                }}

                            >

                                <TextField

                                    fullWidth

                                    multiline

                                    minRows={2}

                                    label="Login Page Subtitle"

                                    name="login_page_subtitle"

                                    value={

                                        settings.login_page_subtitle ??

                                        ""

                                    }

                                    onChange={

                                        handleChange

                                    }

                                    disabled={

                                        disabled

                                    }

                                />

                            </Grid>

                        </Grid>

                    </Stack>

                </Stack>

            </CardContent>

        </Card>

    );

}