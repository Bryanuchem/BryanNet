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

function SubscriptionPurchaseDialog({

    open,

    customers,

    plans,

    onClose,

    onSubmit,

}) {

    const [
        formData,
        setFormData,
    ] = useState({

        customer_id: "",

        plan_id: "",

    });

    useEffect(() => {

        if (!open) {

            return;

        }

        setFormData({

            customer_id: "",

            plan_id: "",

        });

    }, [open]);


    const handleSubmit = () => {

        onSubmit({

            customer_id: Number(
                formData.customer_id,
            ),

            plan_id: Number(
                formData.plan_id,
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

                Purchase Subscription

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

                        <Autocomplete

                            options={customers}

                            value={

                                customers.find(

                                    (customer) =>

                                        customer.customer_id ===

                                        Number(
                                            formData.customer_id,
                                        ),

                                ) ?? null

                            }

                            getOptionLabel={(customer) =>

                                customer.full_name

                            }

                            isOptionEqualToValue={

                                (option, value) =>

                                    option.customer_id ===
                                    value.customer_id

                            }

                            onChange={(_, customer) => {

                                setFormData((previous) => ({

                                    ...previous,

                                    customer_id:

                                        customer?.customer_id ??

                                        "",

                                }));

                            }}

                            renderInput={(params) => (

                                <TextField

                                    {...params}

                                    required

                                    label="Customer"

                                />

                            )}

                        />

                    </Grid>

                    <Grid size={{ xs: 12 }}>

                        <Autocomplete

                            options={plans}

                            value={

                                plans.find(

                                    (plan) =>

                                        plan.plan_id ===

                                        Number(
                                            formData.plan_id,
                                        ),

                                ) ?? null

                            }

                            getOptionLabel={(plan) =>

                                `${plan.plan_name} • ₦${Number(
                                    plan.price,
                                ).toLocaleString()}`

                            }

                            isOptionEqualToValue={

                                (option, value) =>

                                    option.plan_id ===
                                    value.plan_id

                            }

                            onChange={(_, plan) => {

                                setFormData((previous) => ({

                                    ...previous,

                                    plan_id:

                                        plan?.plan_id ??

                                        "",

                                }));

                            }}

                            renderInput={(params) => (

                                <TextField

                                    {...params}

                                    required

                                    label="Plan"

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
                        !formData.customer_id ||
                        !formData.plan_id
                    }
                >

                    Purchase

                </Button>

            </DialogActions>

        </Dialog>

    );

}

export default SubscriptionPurchaseDialog;