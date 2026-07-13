import { useEffect, useState } from "react";

import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Grid,
    TextField,
} from "@mui/material";

const initialForm = {
    full_name: "",
    phone_number: "",
    email: "",
};

function CustomerDialog({
    open,
    onClose,
    onSubmit,
    customer = null,
}) {
    const [formData, setFormData] =
        useState(initialForm);

    useEffect(() => {
        if (!open) return;

        if (customer) {
            setFormData({
                full_name:
                    customer.full_name ?? "",
                phone_number:
                    customer.phone_number ?? "",
                email:
                    customer.email ?? "",
            });
        } else {
            setFormData(initialForm);
        }
    }, [open, customer]);

    const handleChange = (event) => {
        const { name, value } =
            event.target;

        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleSubmit = () => {
        onSubmit(formData);
    };

    return (
        <Dialog
            open={open}
            onClose={onClose}
            fullWidth
            maxWidth="sm"
        >
            <DialogTitle>
                {customer
                    ? "Edit Customer"
                    : "New Customer"}
            </DialogTitle>

            <DialogContent dividers>
                <Grid
                    container
                    spacing={2}
                    sx={{ mt: 0.5 }}
                >
                    <Grid size={{ xs: 12 }}>
                        <TextField
                            fullWidth
                            required
                            label="Full Name"
                            name="full_name"
                            value={
                                formData.full_name
                            }
                            onChange={
                                handleChange
                            }
                        />
                    </Grid>

                    <Grid size={{ xs: 12 }}>
                        <TextField
                            fullWidth
                            required
                            label="Phone Number"
                            name="phone_number"
                            value={
                                formData.phone_number
                            }
                            onChange={
                                handleChange
                            }
                        />
                    </Grid>

                    <Grid size={{ xs: 12 }}>
                        <TextField
                            fullWidth
                            required
                            type="email"
                            label="Email Address"
                            name="email"
                            value={
                                formData.email
                            }
                            onChange={
                                handleChange
                            }
                        />
                    </Grid>

                </Grid>
            </DialogContent>

            <DialogActions>
                <Button onClick={onClose}>
                    Cancel
                </Button>

                <Button
                    variant="contained"
                    onClick={handleSubmit}
                >
                    {customer
                        ? "Save Changes"
                        : "Create Customer"}
                </Button>
            </DialogActions>
        </Dialog>
    );
}

export default CustomerDialog;