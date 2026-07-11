import {
    Card,
    CardContent,
    Divider,
    Grid,
    MenuItem,
    Stack,
    TextField,
    Typography,
} from "@mui/material";

export default function NetworkSettingsForm({

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

            name === "dhcp_lease_time"

                ? Number(

                    value,

                )

                : value,

        );

    }

    return (

        <Card>

            <CardContent>

                <Stack spacing={4}>

                    <Stack spacing={1}>

                        <Typography variant="h6">

                            Network Settings

                        </Typography>

                        <Typography

                            variant="body2"

                            color="text.secondary"

                        >

                            Configure the default networking values used across your BryanNet ISP Platform.

                        </Typography>

                    </Stack>

                    <Divider />

                    <Stack spacing={3}>

                        <Typography

                            variant="subtitle1"

                        >

                            Default Infrastructure

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

                                    label="Default Router"

                                    name="default_router"

                                    value={

                                        settings.default_router ??

                                        ""

                                    }

                                    onChange={

                                        handleChange

                                    }

                                    disabled={

                                        disabled

                                    }

                                    helperText="Default router model or identifier used during device provisioning."

                                />

                            </Grid>

                        </Grid>

                    </Stack>

                    <Divider />

                    <Stack spacing={3}>

                        <Typography

                            variant="subtitle1"

                        >

                            DNS Configuration

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

                                    label="Primary DNS"

                                    name="dns_primary"

                                    value={

                                        settings.dns_primary ??

                                        ""

                                    }

                                    onChange={

                                        handleChange

                                    }

                                    disabled={

                                        disabled

                                    }

                                    helperText="Preferred DNS server."

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

                                    label="Secondary DNS"

                                    name="dns_secondary"

                                    value={

                                        settings.dns_secondary ??

                                        ""

                                    }

                                    onChange={

                                        handleChange

                                    }

                                    disabled={

                                        disabled

                                    }

                                    helperText="Fallback DNS server."

                                />

                            </Grid>

                        </Grid>

                    </Stack>

                    <Divider />

                    <Stack spacing={3}>

                        <Typography

                            variant="subtitle1"

                        >

                            Network Defaults

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

                                    label="DHCP Lease Time (Hours)"

                                    name="dhcp_lease_time"

                                    value={

                                        settings.dhcp_lease_time ??

                                        24

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

                                    select

                                    fullWidth

                                    label="Bandwidth Unit"

                                    name="bandwidth_unit"

                                    value={

                                        settings.bandwidth_unit ??

                                        "Mbps"

                                    }

                                    onChange={

                                        handleChange

                                    }

                                    disabled={

                                        disabled

                                    }

                                >

                                    <MenuItem value="Kbps">

                                        Kbps

                                    </MenuItem>

                                    <MenuItem value="Mbps">

                                        Mbps

                                    </MenuItem>

                                    <MenuItem value="Gbps">

                                        Gbps

                                    </MenuItem>

                                </TextField>

                            </Grid>

                        </Grid>

                    </Stack>

                </Stack>

            </CardContent>

        </Card>

    );

}