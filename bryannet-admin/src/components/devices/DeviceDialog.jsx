import {
    useEffect,
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
} from "@mui/material";

const initialForm = {

    customer_id: "",

    device_name: "",

    mac_address: "",

};

function DeviceDialog({

    open,

    onClose,

    onSubmit,

    customers = [],

}) {

    const [
        formData,
        setFormData,
    ] = useState(initialForm);

    const [
        selectedCustomer,
        setSelectedCustomer,
    ] = useState(null);

    useEffect(() => {

        if (!open) {
            return;
        }

        const nextFormData = {
            customer_id: "",
            device_name: "",
            mac_address: "",
        };

        setFormData((previous) => {

            if (

                previous.customer_id === nextFormData.customer_id &&

                previous.device_name === nextFormData.device_name &&

                previous.mac_address === nextFormData.mac_address

            ) {

                return previous;

            }

            return nextFormData;

        });

    }, [open]);

    const handleChange = (
        event,
    ) => {

        const {

            name,

            value,

        } = event.target;

        setFormData((previous) => ({

            ...previous,

            [name]: value,

        }));

    };

    const handleCustomerChange = (
        event,
        customer,
    ) => {

        setSelectedCustomer(
            customer,
        );

        setFormData((previous) => ({

            ...previous,

            customer_id:
                customer?.customer_id ?? "",

        }));

    };

    const handleSubmit = () => {

        onSubmit(
            formData,
        );

    };

    return (

        <Dialog
            open={open}
            onClose={onClose}
            fullWidth
            maxWidth="sm"
        >

            <DialogTitle>

                Register Device

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

                        <Autocomplete

                            options={customers}

                            value={
                                selectedCustomer
                            }

                            onChange={
                                handleCustomerChange
                            }

                            getOptionLabel={(option) =>
                                option.full_name ?? ""
                            }

                            isOptionEqualToValue={(
                                option,
                                value,
                            ) =>
                                option.customer_id ===
                                value.customer_id
                            }

                            renderInput={(params) => (

                                <TextField
                                    {...params}
                                    required
                                    label="Customer"
                                />

                            )}

                        />

                    </Grid>

                    <Grid
                        size={{
                            xs: 12,
                        }}
                    >

                        <TextField
                            fullWidth
                            required
                            label="Device Name"
                            name="device_name"
                            value={
                                formData.device_name
                            }
                            onChange={
                                handleChange
                            }
                        />

                    </Grid>

                    <Grid
                        size={{
                            xs: 12,
                        }}
                    >

                        <TextField
                            fullWidth
                            required
                            label="MAC Address"
                            name="mac_address"
                            value={
                                formData.mac_address
                            }
                            onChange={
                                handleChange
                            }
                            placeholder="AA:BB:CC:DD:EE:FF"
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

                    Register Device

                </Button>

            </DialogActions>

        </Dialog>

    );

}

export default DeviceDialog;