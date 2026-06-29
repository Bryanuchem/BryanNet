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

    if (!subscription) {
        return null;
    }

    const isView = mode === "view";

    return (

        <Dialog
            open={open}
            onClose={onClose}
            fullWidth
            maxWidth="md"
        >

            <DialogTitle>

                {isView
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
                            size={{
                                xs: 12,
                                md: 6,
                            }}
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
                            size={{
                                xs: 12,
                                md: 6,
                            }}
                        >

                            <TextField
                                fullWidth
                                label="Internet Plan"
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
                            size={{
                                xs: 12,
                                md: 6,
                            }}
                        >

                            <TextField
                                fullWidth
                                label="Start Date"
                                type="date"
                                name="start_date"
                                value={
                                    subscription.start_date?.slice(0, 10) ?? ""
                                }
                                onChange={onChange}
                                InputLabelProps={{
                                    shrink: true,
                                }}
                                InputProps={{
                                    readOnly: isView,
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
                                label="Expiry Date"
                                type="date"
                                name="expiry_date"
                                value={
                                    subscription.expiry_date?.slice(0, 10) ?? ""
                                }
                                onChange={onChange}
                                InputLabelProps={{
                                    shrink: true,
                                }}
                                InputProps={{
                                    readOnly: isView,
                                }}
                            />

                        </Grid>

                        <Grid
                            size={{
                                xs: 12,
                                md: 4,
                            }}
                        >

                            <TextField
                                fullWidth
                                label="Price"
                                value={`₦${Number(
                                    subscription.price ?? 0
                                ).toLocaleString()}`}
                                InputProps={{
                                    readOnly: true,
                                }}
                            />

                        </Grid>

                        <Grid
                            size={{
                                xs: 12,
                                md: 4,
                            }}
                        >

                            <TextField
                                fullWidth
                                label="Remaining Days"
                                value={`${subscription.remaining_days ?? 0} Days`}
                                InputProps={{
                                    readOnly: true,
                                }}
                            />

                        </Grid>

                        <Grid
                            size={{
                                xs: 12,
                                md: 4,
                            }}
                        >

                            <TextField
                                fullWidth
                                label="Activation Queue"
                                name="activation_sequence"
                                type="number"
                                value={
                                    subscription.activation_sequence ?? ""
                                }
                                onChange={onChange}
                                InputProps={{
                                    readOnly: isView,
                                }}
                            />

                        </Grid>

                    </Grid>

                    <Divider />

                    <Stack
                        direction="row"
                        spacing={2}
                        alignItems="center"
                    >

                        <BadgeChip
                            variant="status"
                            value={subscription.status}
                        />

                    </Stack>

                </Stack>

            </DialogContent>

            <DialogActions>

                <Button
                    onClick={onClose}
                >
                    Close
                </Button>

                {!isView && (

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