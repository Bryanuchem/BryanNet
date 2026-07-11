import {
    useEffect,
    useState,
} from "react";

import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Grid,
    TextField,
} from "@mui/material";

function RenameDeviceDialog({

    open,

    device,

    onClose,

    onSubmit,

}) {

    const [

        deviceName,

        setDeviceName,

    ] = useState("");

    useEffect(() => {

        if (!open) {
            return;
        }

        const nextDeviceName =
            device?.device_name ?? "";

        setDeviceName((previous) => {

            if (previous === nextDeviceName) {
                return previous;
            }

            return nextDeviceName;

        });

    }, [open, device]);

    const handleSubmit = () => {

        onSubmit({

            deviceId:
                device.device_id,

            deviceName,

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

                Rename Device

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

                        <TextField
                            fullWidth
                            required
                            label="Device Name"
                            value={deviceName}
                            onChange={(event) =>
                                setDeviceName(
                                    event.target.value,
                                )
                            }
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
                >

                    Rename Device

                </Button>

            </DialogActions>

        </Dialog>

    );

}

export default RenameDeviceDialog;