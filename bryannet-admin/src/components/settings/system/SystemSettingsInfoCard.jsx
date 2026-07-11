import {
    Card,
    CardContent,
    Chip,
    Divider,
    Grid,
    Stack,
    Typography,
} from "@mui/material";

import SettingsSuggestIcon from "@mui/icons-material/SettingsSuggest";

export default function SystemSettingsInfoCard({

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

                        <SettingsSuggestIcon

                            color="primary"

                        />

                        <Typography

                            variant="h6"

                        >

                            System Overview

                        </Typography>

                    </Stack>

                    <Typography

                        variant="body2"

                        color="text.secondary"

                    >

                        Review the current operational state and system-wide retention policies for the BryanNet ISP Platform.

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

                                    Maintenance Mode

                                </Typography>

                                <Chip

                                    color={

                                        settings.maintenance_mode

                                            ? "warning"

                                            : "success"

                                    }

                                    label={

                                        settings.maintenance_mode

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

                                    Debug Mode

                                </Typography>

                                <Chip

                                    color={

                                        settings.debug_mode

                                            ? "warning"

                                            : "success"

                                    }

                                    label={

                                        settings.debug_mode

                                            ? "Enabled"

                                            : "Disabled"

                                    }

                                />

                            </Stack>

                        </Grid>

                        <Grid

                            size={{

                                xs: 12,

                            }}

                        >

                            <Stack spacing={1}>

                                <Typography

                                    variant="caption"

                                    color="text.secondary"

                                >

                                    System Timezone

                                </Typography>

                                <Typography>

                                    {

                                        settings.system_timezone ||

                                        "UTC"

                                    }

                                </Typography>

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

                                    Audit Log Retention

                                </Typography>

                                <Chip

                                    color="primary"

                                    label={`${settings.audit_log_retention_days ?? 90} Days`}

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

                                    Backup Retention

                                </Typography>

                                <Chip

                                    color="primary"

                                    label={`${settings.backup_retention_days ?? 30} Days`}

                                />

                            </Stack>

                        </Grid>

                    </Grid>

                </Stack>

            </CardContent>

        </Card>

    );

}