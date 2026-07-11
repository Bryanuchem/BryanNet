import {
    Card,
    CardContent,
    Divider,
    FormControlLabel,
    Grid,
    Stack,
    Switch,
    TextField,
    Typography,
} from "@mui/material";

export default function AuthenticationSettingsForm({

    settings,

    onChange,

    disabled = false,

}) {

    function handleTextChange(

        event,

    ) {

        const {

            name,

            value,

        } = event.target;

        onChange(

            name,

            Number(

                value,

            ),

        );

    }

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

                            Authentication Settings

                        </Typography>

                        <Typography

                            variant="body2"

                            color="text.secondary"

                        >

                            Configure administrator authentication, password policies and session security.

                        </Typography>

                    </Stack>

                    <Divider />

                    <Stack spacing={3}>

                        <Typography

                            variant="subtitle1"

                        >

                            Registration

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

                                <FormControlLabel

                                    control={

                                        <Switch

                                            name="registration_enabled"

                                            checked={

                                                settings.registration_enabled ??

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

                                    label="Allow New Administrator Registration"

                                />

                            </Grid>

                            <Grid

                                size={{

                                    xs: 12,

                                    md: 6,

                                }}

                            >

                                <FormControlLabel

                                    control={

                                        <Switch

                                            name="two_factor_auth_enabled"

                                            checked={

                                                settings.two_factor_auth_enabled ??

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

                                    label="Require Two-Factor Authentication"

                                />

                            </Grid>

                        </Grid>

                    </Stack>

                    <Divider />

                    <Stack spacing={3}>

                        <Typography

                            variant="subtitle1"

                        >

                            Password Policy

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

                                    type="number"

                                    label="Minimum Password Length"

                                    name="password_min_length"

                                    value={

                                        settings.password_min_length ??

                                        8

                                    }

                                    onChange={

                                        handleTextChange

                                    }

                                    disabled={

                                        disabled

                                    }

                                />

                            </Grid>

                            <Grid

                                size={{

                                    xs: 12,

                                    md: 6,

                                }}

                            />

                            <Grid

                                size={{

                                    xs: 12,

                                    md: 4,

                                }}

                            >

                                <FormControlLabel

                                    control={

                                        <Switch

                                            name="require_uppercase"

                                            checked={

                                                settings.require_uppercase ??

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

                                    label="Require Uppercase"

                                />

                            </Grid>

                            <Grid

                                size={{

                                    xs: 12,

                                    md: 4,

                                }}

                            >

                                <FormControlLabel

                                    control={

                                        <Switch

                                            name="require_numbers"

                                            checked={

                                                settings.require_numbers ??

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

                                    label="Require Numbers"

                                />

                            </Grid>

                            <Grid

                                size={{

                                    xs: 12,

                                    md: 4,

                                }}

                            >

                                <FormControlLabel

                                    control={

                                        <Switch

                                            name="require_special_characters"

                                            checked={

                                                settings.require_special_characters ??

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

                                    label="Require Special Characters"

                                />

                            </Grid>

                        </Grid>

                    </Stack>

                    <Divider />

                    <Stack spacing={3}>

                        <Typography

                            variant="subtitle1"

                        >

                            Session Security

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

                                    type="number"

                                    label="Maximum Login Attempts"

                                    name="max_login_attempts"

                                    value={

                                        settings.max_login_attempts ??

                                        5

                                    }

                                    onChange={

                                        handleTextChange

                                    }

                                    disabled={

                                        disabled

                                    }

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

                                    type="number"

                                    label="Session Timeout (Minutes)"

                                    name="session_timeout_minutes"

                                    value={

                                        settings.session_timeout_minutes ??

                                        30

                                    }

                                    onChange={

                                        handleTextChange

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