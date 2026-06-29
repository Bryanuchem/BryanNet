import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Divider,
    Grid,
    Stack,
    TextField,
} from "@mui/material";

import BadgeChip from "../common/BadgeChip";

function SubscriptionDialog({
    open,
    mode = "view",
    subscription,
    onClose,
    onSave,
    onChange,
}) {

    const readOnly = mode === "view";

    if (!subscription) {
        return null;
    }

    return (
        <Dialog
            open={open}
            onClose={onClose}
            fullWidth
            maxWidth="sm"
        >

            <DialogTitle>

                {mode === "view"
                    ? "Subscription Details"
                    : "Edit Subscription"}

            </DialogTitle>

            <DialogContent>

                <Stack
                    spacing={3}
                    sx={{ mt: 1 }}
                >

                    <Grid
                        container
                        spacing={2}
                    >

                        <Grid
                            item
                            xs={12}
                        >

                            <TextField
                                fullWidth
                                label="Customer"
                                value={
                                    subscription.customer_name ?? ""
                                }
                                InputProps={{
                                    readOnly: true,
                                }}
                            />

                        </Grid>

                        <Grid
                            item
                            xs={12}
                        >

                            <TextField
                                fullWidth
                                label="Plan"
                                value={
                                    subscription.plan_name ?? ""
                                }
                                InputProps={{
                                    readOnly: true,
                                }}
                            />

                        </Grid>

                    </Grid>

                    <Divider />

                    <Grid
                        container
                        spacing={2}
                    >

                        <Grid
                            item
                            xs={6}
                        >

                            <TextField
                                fullWidth
                                label="Start Date"
                                type="date"
                                value={
                                    subscription.start_date
                                        ?.slice(0, 10) ?? ""
                                }
                                onChange={onChange}
                                name="start_date"
                                InputLabelProps={{
                                    shrink: true,
                                }}
                                InputProps={{
                                    readOnly,
                                }}
                            />

                        </Grid>

                        <Grid
                            item
                            xs={6}
                        >

                            <TextField
                                fullWidth
                                label="Expiry Date"
                                type="date"
                                value={
                                    subscription.expiry_date
                                        ?.slice(0, 10) ?? ""
                                }
                                onChange={onChange}
                                name="expiry_date"
                                InputLabelProps={{
                                    shrink: true,
                                }}
                                InputProps={{
                                    readOnly,
                                }}
                            />

                        </Grid>

                        <Grid
                            item
                            xs={6}
                        >

                            <TextField
                                fullWidth
                                label="Activation Sequence"
                                name="activation_sequence"
                                type="number"
                                value={
                                    subscription.activation_sequence ?? ""
                                }
                                onChange={onChange}
                                InputProps={{
                                    readOnly,
                                }}
                            />

                        </Grid>

                        <Grid
                            item
                            xs={6}
                        >

                            <Stack
                                sx={{ mt: 1 }}
                            >

                                <BadgeChip
                                    variant="status"
                                    value={
                                        subscription.status
                                    }
                                />

                            </Stack>

                        </Grid>

                    </Grid>

                </Stack>

            </DialogContent>

            <DialogActions>

                <Button
                    onClick={onClose}
                >
                    Close
                </Button>

                {mode === "edit" && (

                    <Button
                        variant="contained"
                        onClick={onSave}
                    >
                        Save Changes
                    </Button>

                )}

            </DialogActions>

        </Dialog>
    );

}

export default SubscriptionDialog;