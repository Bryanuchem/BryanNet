import {

    useState,

} from "react";

import {
    Card,
    CardContent,
    Divider,
    FormControlLabel,
    Grid,
    IconButton,
    InputAdornment,
    MenuItem,
    Stack,
    Switch,
    TextField,
    Typography,
} from "@mui/material";

import VisibilityIcon from "@mui/icons-material/Visibility";
import VisibilityOffIcon from "@mui/icons-material/VisibilityOff";

export default function IntegrationSettingsForm({

    settings,

    onChange,

    disabled = false,

}) {

    const [

        showSmtpPassword,

        setShowSmtpPassword,

    ] = useState(

        false,

    );

    const [

        showSmsApiKey,

        setShowSmsApiKey,

    ] = useState(

        false,

    );

    function handleChange(

        event,

    ) {

        const {

            name,

            value,

        } = event.target;

        onChange(

            name,

            name === "smtp_port"

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

                            Integration Settings

                        </Typography>

                        <Typography

                            variant="body2"

                            color="text.secondary"

                        >

                            Configure email and SMS providers used for platform notifications and communications.

                        </Typography>

                    </Stack>

                    <Divider />

                    <Stack spacing={3}>

                        <Typography

                            variant="subtitle1"

                        >

                            Email (SMTP)

                        </Typography>

                        <Grid

                            container

                            spacing={3}

                        >

                            <Grid

                                size={{

                                    xs: 12,

                                    md: 8,

                                }}

                            >

                                <TextField

                                    fullWidth

                                    label="SMTP Host"

                                    name="smtp_host"

                                    value={

                                        settings.smtp_host ??

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

                                    fullWidth

                                    type="number"

                                    label="SMTP Port"

                                    name="smtp_port"

                                    value={

                                        settings.smtp_port ??

                                        587

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

                                    label="SMTP Username"

                                    name="smtp_username"

                                    value={

                                        settings.smtp_username ??

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

                                    label="SMTP Password"

                                    name="smtp_password"

                                    type={

                                        showSmtpPassword

                                            ? "text"

                                            : "password"

                                    }

                                    value={

                                        settings.smtp_password ??

                                        ""

                                    }

                                    onChange={

                                        handleChange

                                    }

                                    disabled={

                                        disabled

                                    }

                                    InputProps={{

                                        endAdornment: (

                                            <InputAdornment position="end">

                                                <IconButton

                                                    edge="end"

                                                    onClick={() =>

                                                        setShowSmtpPassword(

                                                            (

                                                                previous,

                                                            ) =>

                                                                !previous,

                                                        )

                                                    }

                                                >

                                                    {

                                                        showSmtpPassword

                                                            ? (

                                                                <VisibilityOffIcon />

                                                            ) : (

                                                                <VisibilityIcon />

                                                            )

                                                    }

                                                </IconButton>

                                            </InputAdornment>

                                        ),

                                    }}

                                />

                            </Grid>

                            <Grid

                                size={{

                                    xs: 12,

                                }}

                            >

                                <FormControlLabel

                                    control={

                                        <Switch

                                            name="smtp_use_tls"

                                            checked={

                                                settings.smtp_use_tls ??

                                                true

                                            }

                                            onChange={

                                                handleSwitchChange

                                            }

                                            disabled={

                                                disabled

                                            }

                                        />

                                    }

                                    label="Use TLS Encryption"

                                />

                            </Grid>

                        </Grid>

                    </Stack>

                    <Divider />

                    <Stack spacing={3}>

                        <Typography

                            variant="subtitle1"

                        >

                            SMS Provider

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

                                    label="SMS Provider"

                                    name="sms_provider"

                                    value={

                                        settings.sms_provider ??

                                        ""

                                    }

                                    onChange={

                                        handleChange

                                    }

                                    disabled={

                                        disabled

                                    }

                                >

                                    <MenuItem value="">

                                        None

                                    </MenuItem>

                                    <MenuItem value="Twilio">

                                        Twilio

                                    </MenuItem>

                                    <MenuItem value="Termii">

                                        Termii

                                    </MenuItem>

                                    <MenuItem value="Africa's Talking">

                                        Africa's Talking

                                    </MenuItem>

                                    <MenuItem value="Custom">

                                        Custom

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

                            API Configuration

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

                                    label="SMS API Key"

                                    name="sms_api_key"

                                    type={

                                        showSmsApiKey

                                            ? "text"

                                            : "password"

                                    }

                                    value={

                                        settings.sms_api_key ??

                                        ""

                                    }

                                    onChange={

                                        handleChange

                                    }

                                    disabled={

                                        disabled

                                    }

                                    InputProps={{

                                        endAdornment: (

                                            <InputAdornment position="end">

                                                <IconButton

                                                    edge="end"

                                                    onClick={() =>

                                                        setShowSmsApiKey(

                                                            (

                                                                previous,

                                                            ) =>

                                                                !previous,

                                                        )

                                                    }

                                                >

                                                    {

                                                        showSmsApiKey

                                                            ? (

                                                                <VisibilityOffIcon />

                                                            ) : (

                                                                <VisibilityIcon />

                                                            )

                                                    }

                                                </IconButton>

                                            </InputAdornment>

                                        ),

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