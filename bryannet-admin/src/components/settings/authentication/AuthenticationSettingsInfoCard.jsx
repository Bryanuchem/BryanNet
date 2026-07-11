import {
    Card,
    CardContent,
    Chip,
    Divider,
    Grid,
    Stack,
    Typography,
} from "@mui/material";

import SecurityIcon from "@mui/icons-material/Security";

export default function AuthenticationSettingsInfoCard({

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

                        <SecurityIcon

                            color="primary"

                        />

                        <Typography

                            variant="h6"

                        >

                            Authentication Overview

                        </Typography>

                    </Stack>

                    <Typography

                        variant="body2"

                        color="text.secondary"

                    >

                        Review the current authentication and security policies that protect administrator access to the BryanNet ISP Platform.

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

                                    Registration

                                </Typography>

                                <Chip

                                    color={

                                        settings.registration_enabled

                                            ? "success"

                                            : "default"

                                    }

                                    label={

                                        settings.registration_enabled

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

                                    Two-Factor Authentication

                                </Typography>

                                <Chip

                                    color={

                                        settings.two_factor_auth_enabled

                                            ? "success"

                                            : "warning"

                                    }

                                    label={

                                        settings.two_factor_auth_enabled

                                            ? "Enabled"

                                            : "Disabled"

                                    }

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

                                    Password Length

                                </Typography>

                                <Typography>

                                    {

                                        settings.password_min_length

                                    } Characters

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

                                    Login Attempts

                                </Typography>

                                <Typography>

                                    {

                                        settings.max_login_attempts

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

                                    Session Timeout

                                </Typography>

                                <Typography>

                                    {

                                        settings.session_timeout_minutes

                                    } Minutes

                                </Typography>

                            </Stack>

                        </Grid>

                    </Grid>

                    <Divider />

                    <Stack spacing={1}>

                        <Typography

                            variant="subtitle2"

                        >

                            Password Requirements

                        </Typography>

                        <Stack

                            direction="row"

                            spacing={1}

                            flexWrap="wrap"

                        >

                            <Chip

                                size="small"

                                color={

                                    settings.require_uppercase

                                        ? "success"

                                        : "default"

                                }

                                label="Uppercase"

                            />

                            <Chip

                                size="small"

                                color={

                                    settings.require_numbers

                                        ? "success"

                                        : "default"

                                }

                                label="Numbers"

                            />

                            <Chip

                                size="small"

                                color={

                                    settings.require_special_characters

                                        ? "success"

                                        : "default"

                                }

                                label="Special Characters"

                            />

                        </Stack>

                    </Stack>

                </Stack>

            </CardContent>

        </Card>

    );

}