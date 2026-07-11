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

export default function BillingSettingsForm({

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
                "invoice_due_days",
                "suspend_after_days",
                "tax_percentage",
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

                            Billing Settings

                        </Typography>

                        <Typography

                            variant="body2"

                            color="text.secondary"

                        >

                            Configure default payment options, invoice policies and customer suspension rules.

                        </Typography>

                    </Stack>

                    <Divider />

                    <Stack spacing={3}>

                        <Typography

                            variant="subtitle1"

                        >

                            Payment Defaults

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

                                    label="Default Payment Method"

                                    name="default_payment_method"

                                    value={

                                        settings.default_payment_method ??

                                        ""

                                    }

                                    onChange={

                                        handleTextChange

                                    }

                                    disabled={

                                        disabled

                                    }

                                >

                                    <MenuItem value="Cash">

                                        Cash

                                    </MenuItem>

                                    <MenuItem value="Transfer">

                                        Bank Transfer

                                    </MenuItem>

                                    <MenuItem value="Card">

                                        Card

                                    </MenuItem>

                                    <MenuItem value="Wallet">

                                        Wallet

                                    </MenuItem>

                                </TextField>

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

                                    label="Default Payment Channel"

                                    name="default_payment_channel"

                                    value={

                                        settings.default_payment_channel ??

                                        ""

                                    }

                                    onChange={

                                        handleTextChange

                                    }

                                    disabled={

                                        disabled

                                    }

                                >

                                    <MenuItem value="Manual">

                                        Manual

                                    </MenuItem>

                                    <MenuItem value="Paystack">

                                        Paystack

                                    </MenuItem>

                                    <MenuItem value="Flutterwave">

                                        Flutterwave

                                    </MenuItem>

                                    <MenuItem value="Monnify">

                                        Monnify

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

                            Invoice Rules

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

                                    label="Invoice Due Days"

                                    name="invoice_due_days"

                                    value={

                                        settings.invoice_due_days ??

                                        7

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

                                    label="Suspend After Days"

                                    name="suspend_after_days"

                                    value={

                                        settings.suspend_after_days ??

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

                    <Divider />

                    <Stack spacing={3}>

                        <Typography

                            variant="subtitle1"

                        >

                            Suspension & Tax

                        </Typography>

                        <Grid

                            container

                            spacing={3}

                            alignItems="center"

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

                                            name="auto_suspend_overdue"

                                            checked={

                                                settings.auto_suspend_overdue ??

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

                                    label="Automatically Suspend Overdue Customers"

                                />

                                <Typography

                                    variant="body2"

                                    color="text.secondary"

                                    sx={{

                                        mt: 1,

                                    }}

                                >

                                    Automatically suspend customer services once the configured overdue period has elapsed.

                                </Typography>

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

                                    label="Tax Percentage"

                                    name="tax_percentage"

                                    value={

                                        settings.tax_percentage ??

                                        0

                                    }

                                    onChange={

                                        handleTextChange

                                    }

                                    disabled={

                                        disabled

                                    }

                                    inputProps={{

                                        min: 0,

                                        max: 100,

                                        step: 0.01,

                                    }}

                                    helperText="Applied to invoices by default."

                                />

                            </Grid>

                        </Grid>

                    </Stack>

                </Stack>

            </CardContent>

        </Card>

    );

}