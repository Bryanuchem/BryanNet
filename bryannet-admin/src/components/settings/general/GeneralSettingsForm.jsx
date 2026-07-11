import {
    Card,
    CardContent,
    Grid,
    MenuItem,
    Stack,
    TextField,
    Typography,
} from "@mui/material";

export default function GeneralSettingsForm({

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

                <Stack spacing={3}>

                    <Typography variant="h6">

                        General Settings

                    </Typography>

                    <Typography

                        variant="body2"

                        color="text.secondary"

                    >

                        Configure your organization's primary information and regional preferences.

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

                                required

                                label="Platform Name"

                                name="platform_name"

                                value={

                                    settings.platform_name ??

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

                                md: 6,

                            }}

                        >

                            <TextField

                                fullWidth

                                required

                                label="Company Name"

                                name="company_name"

                                value={

                                    settings.company_name  ??

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

                                md: 6,

                            }}

                        >

                            <TextField

                                fullWidth

                                required

                                type="email"

                                label="Company Email"

                                name="company_email"

                                value={

                                    settings.company_email  ??

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

                                md: 6,

                            }}

                        >

                            <TextField

                                fullWidth

                                label="Company Phone"

                                name="company_phone"

                                value={

                                    settings.company_phone  ??

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

                                md: 4,

                            }}

                        >

                            <TextField

                                select

                                fullWidth

                                label="Time Zone"

                                name="default_timezone"

                                value={

                                    settings.default_timezone  ??

                                    "UTC"

                                }

                                onChange={

                                    handleChange

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

                        <Grid

                            size={{

                                xs: 12,

                                md: 4,

                            }}

                        >

                            <TextField

                                select

                                fullWidth

                                label="Date Format"

                                name="date_format"

                                value={

                                    settings.date_format  ??

                                    "DD/MM/YYYY"

                                }

                                onChange={

                                    handleChange

                                }

                                disabled={

                                    disabled

                                }

                            >

                                <MenuItem value="DD/MM/YYYY">

                                    DD/MM/YYYY

                                </MenuItem>

                                <MenuItem value="MM/DD/YYYY">

                                    MM/DD/YYYY

                                </MenuItem>

                                <MenuItem value="YYYY-MM-DD">

                                    YYYY-MM-DD

                                </MenuItem>

                            </TextField>

                        </Grid>

                        <Grid

                            size={{

                                xs: 12,

                                md: 4,

                            }}

                        >

                            <TextField

                                select

                                fullWidth

                                label="Currency"

                                name="default_currency"

                                value={

                                    settings.default_currency ??

                                    "NGN"

                                }

                                onChange={

                                    handleChange

                                }

                                disabled={

                                    disabled

                                }

                            >

                                <MenuItem value="NGN">

                                    Nigerian Naira (₦)

                                </MenuItem>

                                <MenuItem value="USD">

                                    US Dollar ($)

                                </MenuItem>

                                <MenuItem value="EUR">

                                    Euro (€)

                                </MenuItem>

                                <MenuItem value="GBP">

                                    British Pound (£)

                                </MenuItem>

                            </TextField>

                        </Grid>

                    </Grid>

                </Stack>

            </CardContent>

        </Card>

    );

}