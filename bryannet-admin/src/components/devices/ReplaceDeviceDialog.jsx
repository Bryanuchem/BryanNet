import {
    useEffect,
    useMemo,
    useState,
} from "react";

import {
    Autocomplete,
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Grid,
    TextField,
    Typography,
} from "@mui/material";

function ReplaceDeviceDialog({

    open,

    device,

    devices = [],

    onClose,

    onSubmit,

}) {

    const [

        replacement,

        setReplacement,

    ] = useState(null);

    useEffect(() => {

        if (!open) {
            return;
        }

        const nextReplacement = {
            new_device_id: "",
        };

        setReplacement((previous) => {

            if (
                previous.new_device_id ===
                nextReplacement.new_device_id
            ) {
                return previous;
            }

            return nextReplacement;

        });

    }, [open]);

    const availableDevices =
        useMemo(() => {

            if (!device) {

                return [];

            }

            return devices.filter(

                (candidate) =>

                    candidate.customer_id ===
                    device.customer_id

                    &&

                    candidate.device_id !==
                    device.device_id,

            );

        }, [

            devices,

            device,

        ]);

    const handleSubmit = () => {

        if (!replacement) {

            return;

        }

        onSubmit({

            customer_id:
                device.customer_id,

            old_device_id:
                device.device_id,

            new_device_id:
                replacement.device_id,

        });

    };

    return (

        <Dialog
            open={open}
            onClose={onClose}
            fullWidth
            maxWidth="sm"
        >

            <DialogTitle>

                Replace Device

            </DialogTitle>

            <DialogContent dividers>

                <Grid
                    container
                    spacing={2}
                    sx={{
                        mt: 0.5,
                    }}
                >

                    <Grid
                        size={{
                            xs: 12,
                        }}
                    >

                        <Typography
                            color="text.secondary"
                        >

                            Current Device

                        </Typography>

                        <Typography
                            fontWeight={600}
                        >

                            {device?.device_name}

                        </Typography>

                    </Grid>

                    <Grid
                        size={{
                            xs: 12,
                        }}
                    >

                        <Autocomplete

                            options={
                                availableDevices
                            }

                            value={
                                replacement
                            }

                            onChange={(
                                event,
                                value,
                            ) =>
                                setReplacement(
                                    value,
                                )
                            }

                            getOptionLabel={(option) =>
                                `${option.device_name} (${option.mac_address})`
                            }

                            isOptionEqualToValue={(
                                option,
                                value,
                            ) =>
                                option.device_id ===
                                value.device_id
                            }

                            renderInput={(params) => (

                                <TextField
                                    {...params}
                                    label="Replacement Device"
                                    required
                                />

                            )}

                        />

                    </Grid>

                </Grid>

            </DialogContent>

            <DialogActions>

                <Button
                    onClick={onClose}
                >

                    Cancel

                </Button>

                <Button
                    variant="contained"
                    onClick={handleSubmit}
                    disabled={
                        !replacement
                    }
                >

                    Replace Device

                </Button>

            </DialogActions>

        </Dialog>

    );

}

export default ReplaceDeviceDialog;