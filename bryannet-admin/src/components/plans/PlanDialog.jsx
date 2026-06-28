import { useEffect, useState } from "react";

import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    FormControlLabel,
    Grid,
    Switch,
    TextField,
} from "@mui/material";

const initialForm = {
    plan_name: "",
    price: "",
    duration_days: "",
    speed_limit_mbps: "",
    max_devices: "",
    concurrent_devices: "",
    is_active: true,
};

const PlanDialog = ({
    open,
    onClose,
    onSubmit,
    plan = null,
}) => {
    const [formData, setFormData] = useState(initialForm);

    useEffect(() => {
        if (!open) return;

        if (plan) {
            setFormData({
                plan_name: plan.plan_name,
                price: plan.price,
                duration_days: plan.duration_days,
                speed_limit_mbps: plan.speed_limit_mbps,
                max_devices: plan.max_devices,
                concurrent_devices: plan.concurrent_devices,
                is_active: plan.is_active,
            });
        } else {
            setFormData(initialForm);
        }
    }, [open, plan]);

    const handleChange = (event) => {
        const { name, value } = event.target;

        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleSwitchChange = (event) => {
        setFormData((prev) => ({
            ...prev,
            is_active: event.target.checked,
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
                {plan ? "Edit Plan" : "Create New Plan"}
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
                            label="Plan Name"
                            name="plan_name"
                            value={formData.plan_name}
                            onChange={handleChange}
                        />
                    </Grid>

                    <Grid size={{ xs: 12, sm: 6 }}>
                        <TextField
                            fullWidth
                            type="number"
                            label="Price (₦)"
                            name="price"
                            value={formData.price}
                            onChange={handleChange}
                        />
                    </Grid>

                    <Grid size={{ xs: 12, sm: 6 }}>
                        <TextField
                            fullWidth
                            type="number"
                            label="Duration (Days)"
                            name="duration_days"
                            value={formData.duration_days}
                            onChange={handleChange}
                        />
                    </Grid>

                    <Grid size={{ xs: 12, sm: 6 }}>
                        <TextField
                            fullWidth
                            type="number"
                            label="Speed Limit (Mbps)"
                            name="speed_limit_mbps"
                            value={formData.speed_limit_mbps}
                            onChange={handleChange}
                        />
                    </Grid>

                    <Grid size={{ xs: 12, sm: 6 }}>
                        <TextField
                            fullWidth
                            type="number"
                            label="Maximum Devices"
                            name="max_devices"
                            value={formData.max_devices}
                            onChange={handleChange}
                        />
                    </Grid>

                    <Grid size={{ xs: 12, sm: 6 }}>
                        <TextField
                            fullWidth
                            type="number"
                            label="Concurrent Devices"
                            name="concurrent_devices"
                            value={formData.concurrent_devices}
                            onChange={handleChange}
                        />
                    </Grid>

                    <Grid size={{ xs: 12 }}>
                        <FormControlLabel
                            control={
                                <Switch
                                    checked={formData.is_active}
                                    onChange={handleSwitchChange}
                                />
                            }
                            label="Plan is Active"
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
                    {plan ? "Save Changes" : "Save"}
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default PlanDialog;