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
    Switch,
    FormControlLabel,
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

function PlanDialog({

    open,

    onClose,

    onSubmit,

    plan = null,

}) {

    const [
        formData,
        setFormData,
    ] = useState(initialForm);

    useEffect(() => {

        if (!open) {
            return;
        }

        const nextFormData = plan

            ? {

                  plan_name:
                      plan.plan_name ?? "",

                  price:
                      plan.price ?? "",

                  duration_days:
                      plan.duration_days ?? "",

                  speed_limit_mbps:
                      plan.speed_limit_mbps ?? "",

                  max_devices:
                      plan.max_devices ?? "",

                  concurrent_devices:
                      plan.concurrent_devices ?? "",

                  is_active:
                      plan.is_active ?? true,

              }

            : initialForm;

        setFormData((previous) => {

            if (

                previous.plan_name ===
                    nextFormData.plan_name &&

                previous.price ===
                    nextFormData.price &&

                previous.duration_days ===
                    nextFormData.duration_days &&

                previous.speed_limit_mbps ===
                    nextFormData.speed_limit_mbps &&

                previous.max_devices ===
                    nextFormData.max_devices &&

                previous.concurrent_devices ===
                    nextFormData.concurrent_devices &&

                previous.is_active ===
                    nextFormData.is_active

            ) {

                return previous;

            }

            return nextFormData;

        });

    }, [open, plan]);

    const handleChange = (
        event,
    ) => {

        const {

            name,

            value,

            type,

            checked,

        } = event.target;

        setFormData((previous) => ({

            ...previous,

            [name]:

                type === "checkbox"

                    ? checked

                    : value,

        }));

    };

    const handleSubmit = () => {

        onSubmit({

            ...formData,

            price:
                Number(formData.price),

            duration_days:
                Number(formData.duration_days),

            speed_limit_mbps:
                Number(formData.speed_limit_mbps),

            max_devices:
                Number(formData.max_devices),

            concurrent_devices:
                Number(formData.concurrent_devices),

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

                {plan

                    ? "Edit Plan"

                    : "New Plan"}

            </DialogTitle>

            <DialogContent dividers>

                <Grid
                    container
                    spacing={2}
                    sx={{
                        mt: 0.5,
                    }}
                >

                    <Grid size={{ xs: 12 }}>

                        <TextField
                            fullWidth
                            required
                            label="Plan Name"
                            name="plan_name"
                            value={formData.plan_name}
                            onChange={handleChange}
                        />

                    </Grid>

                    <Grid size={{ xs: 6 }}>

                        <TextField
                            fullWidth
                            required
                            type="number"
                            label="Price"
                            name="price"
                            value={formData.price}
                            onChange={handleChange}
                        />

                    </Grid>

                    <Grid size={{ xs: 6 }}>

                        <TextField
                            fullWidth
                            required
                            type="number"
                            label="Duration (Days)"
                            name="duration_days"
                            value={formData.duration_days}
                            onChange={handleChange}
                        />

                    </Grid>

                    <Grid size={{ xs: 6 }}>

                        <TextField
                            fullWidth
                            required
                            type="number"
                            label="Speed (Mbps)"
                            name="speed_limit_mbps"
                            value={formData.speed_limit_mbps}
                            onChange={handleChange}
                        />

                    </Grid>

                    <Grid size={{ xs: 6 }}>

                        <TextField
                            fullWidth
                            required
                            type="number"
                            label="Max Devices"
                            name="max_devices"
                            value={formData.max_devices}
                            onChange={handleChange}
                        />

                    </Grid>

                    <Grid size={{ xs: 6 }}>

                        <TextField
                            fullWidth
                            required
                            type="number"
                            label="Concurrent Devices"
                            name="concurrent_devices"
                            value={
                                formData.concurrent_devices
                            }
                            onChange={handleChange}
                        />

                    </Grid>

                    <Grid size={{ xs: 12 }}>

                        <FormControlLabel

                            control={

                                <Switch

                                    name="is_active"

                                    checked={
                                        formData.is_active
                                    }

                                    onChange={
                                        handleChange
                                    }

                                />

                            }

                            label="Plan Active"

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

                    {plan

                        ? "Save Changes"

                        : "Create Plan"}

                </Button>

            </DialogActions>

        </Dialog>

    );

}

export default PlanDialog;