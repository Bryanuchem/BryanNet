import {
    Card,
    CardContent,
    Divider,
    FormControlLabel,
    Grid,
    MenuItem,
    Stack,
    Switch,
    TextField,
    Typography,
} from "@mui/material";

export default function SystemSettingsForm({

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

            [

                "audit_log_retention_days",

                "backup_retention_days",

            ].includes(

                name,

            )

                ? Number(

                    value,

                )

                : value,

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

                            System Settings

                        </Typography>

                        <Typography

                            variant="body2"

                            color="text.secondary"

                        >

                            Configure global platform behaviour, maintenance options and data retention policies.

                        </Typography>

                    </Stack>

                    <Divider />

                    <Stack spacing={3}>

                        <Typography

                            variant="subtitle1"

                        >

                            System Status

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

                                                name="maintenance_mode"

                                                checked={

                                                    settings.maintenance_mode ??

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

                                        label="Maintenance Mode"

                                    />

                                    <Typography

                                        variant="body2"

                                        color="text.secondary"

                                    >

                                        Prevent normal platform access while maintenance is being performed.

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

                                                name="debug_mode"

                                                checked={

                                                    settings.debug_mode ??

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

                                        label="Debug Mode"

                                    />

                                    <Typography

                                        variant="body2"

                                        color="text.secondary"

                                    >

                                        Enable additional debugging information. Recommended only for development environments.

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

                            Regional Settings

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

                                    select

                                    fullWidth

                                    label="System Timezone"

                                    name="system_timezone"

                                    value={

                                        settings.system_timezone ??

                                        "UTC"

                                    }

                                    onChange={

                                        handleTextChange

                                    }

                                    disabled={

                                        disabled

                                    }

                                >

                                    <MenuItem value="UTC">

                                        UTC

                                    </MenuItem>

                                    <MenuItem value="Africa/Lagos">

                                        Africa/Lagos

                                    </MenuItem>

                                    <MenuItem value="Europe/London">

                                        Europe/London

                                    </MenuItem>

                                    <MenuItem value="America/New_York">

                                        America/New_York

                                    </MenuItem>

                                </TextField>

                            </Grid>

                        </Grid>

                    </Stack>

                    <Divider />

                    <Stack spacing={3}>

                        <Typography

                            variant="subtitle1"

                        >

                            Data Retention

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

                                    label="Audit Log Retention (Days)"

                                    name="audit_log_retention_days"

                                    value={

                                        settings.audit_log_retention_days ??

                                        90

                                    }

                                    onChange={

                                        handleTextChange

                                    }

                                    disabled={

                                        disabled

                                    }

                                    inputProps={{

                                        min: 1,

                                    }}

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

                                    label="Backup Retention (Days)"

                                    name="backup_retention_days"

                                    value={

                                        settings.backup_retention_days ??

                                        30

                                    }

                                    onChange={

                                        handleTextChange

                                    }

                                    disabled={

                                        disabled

                                    }

                                    inputProps={{

                                        min: 1,

                                    }}

                                />

                            </Grid>

                        </Grid>

                    </Stack>

                </Stack>

            </CardContent>

        </Card>

    );

}