import { useEffect, useState } from "react";

import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    FormControl,
    InputLabel,
    MenuItem,
    Select,
    Stack,
    TextField,
} from "@mui/material";

const INITIAL_FORM_DATA = {
    customer_id: "",
    device_name: "",
    mac_address: "",
};

function DeviceDialog({
    open,
    customers = [],
    onClose,
    onSubmit,
}) {
    const [formData, setFormData] =
        useState(INITIAL_FORM_DATA);

    useEffect(() => {
        if (open) {
            setFormData(INITIAL_FORM_DATA);
        }
    }, [open]);

    const handleChange = (event) => {
        const { name, value } = event.target;

        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleSubmit = () => {
        onSubmit({
            ...formData,
            customer_id: Number(
                formData.customer_id
            ),
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
                Register Device
            </DialogTitle>

            <DialogContent>

                <Stack
                    spacing={3}
                    sx={{ mt: 1 }}
                >

                    <FormControl fullWidth>

                        <InputLabel>
                            Customer
                        </InputLabel>

                        <Select
                            name="customer_id"
                            value={
                                formData.customer_id
                            }
                            label="Customer"
                            onChange={handleChange}
                        >

                            {customers.map(
                                (customer) => (

                                    <MenuItem
                                        key={
                                            customer.customer_id
                                        }
                                        value={
                                            customer.customer_id
                                        }
                                    >
                                        {customer.full_name}
                                    </MenuItem>

                                )
                            )}

                        </Select>

                    </FormControl>

                    <TextField
                        fullWidth
                        label="Device Name"
                        name="device_name"
                        value={
                            formData.device_name
                        }
                        onChange={handleChange}
                    />

                    <TextField
                        fullWidth
                        label="MAC Address"
                        name="mac_address"
                        value={
                            formData.mac_address
                        }
                        onChange={handleChange}
                    />

                </Stack>

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
                    Register
                </Button>

            </DialogActions>

        </Dialog>
    );
}

export default DeviceDialog;