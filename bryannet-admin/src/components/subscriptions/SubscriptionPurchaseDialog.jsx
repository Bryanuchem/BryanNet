import {
    Autocomplete,
    Box,
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Divider,
    MenuItem,
    Paper,
    Stack,
    TextField,
    Typography,
} from "@mui/material";

function SubscriptionPurchaseDialog({
    open,
    customers = [],
    plans = [],
    subscription,
    onChange,
    onClose,
    onPurchase,
}) {

    const selectedPlan = plans.find(
        (plan) =>
            Number(plan.plan_id) ===
            Number(subscription?.plan_id)
    );

    const selectedCustomer =
        customers.find(
            (customer) =>
                Number(customer.customer_id) ===
                Number(subscription?.customer_id)
        ) || null;

    return (

        <Dialog
            open={open}
            onClose={onClose}
            fullWidth
            maxWidth="sm"
        >

            <DialogTitle>
                New Subscription
            </DialogTitle>

            <DialogContent>

                <Stack
                    spacing={3}
                    sx={{ mt: 1 }}
                >

                    <Autocomplete
                        fullWidth
                        options={customers}
                        value={selectedCustomer}
                        isOptionEqualToValue={(option, value) =>
                            option.customer_id === value.customer_id
                        }
                        getOptionLabel={(option) =>
                            `${option.full_name ?? ""} (${option.phone_number ?? "No Phone"})`
                        }
                        filterOptions={(options, state) => {

                            const search = state.inputValue
                                .toLowerCase()
                                .trim();

                            return options.filter((customer) =>

                                (customer.full_name ?? "")
                                    .toLowerCase()
                                    .includes(search)

                                ||

                                (customer.phone_number ?? "")
                                    .toLowerCase()
                                    .includes(search)

                                ||

                                String(customer.customer_id)
                                    .includes(search)

                            );

                        }}                        
                        onChange={(event, customer) => {

                            onChange({
                                target: {
                                    name: "customer_id",
                                    value: customer
                                        ? customer.customer_id
                                        : "",
                                },
                            });

                        }}
                        renderOption={(props, option) => (

                            <li
                                {...props}
                                key={option.customer_id}
                            >

                                <Box>

                                    <Typography
                                        fontWeight={600}
                                    >
                                        {option.full_name}
                                    </Typography>

                                    <Typography
                                        variant="caption"
                                        color="text.secondary"
                                    >
                                        {option.phone_number ?? "No phone number"}
                                    </Typography>

                                    <Typography
                                        variant="caption"
                                        display="block"
                                        color="text.secondary"
                                    >
                                        Customer #{option.customer_id}
                                    </Typography>

                                </Box>

                            </li>

                        )}                        
                        renderInput={(params) => (

                            <TextField
                                {...params}
                                label="Customer"
                                placeholder="Search by name, phone or customer ID..."
                            />

                        )}
                    />

                    <TextField
                        select
                        fullWidth
                        label="Internet Plan"
                        name="plan_id"
                        value={
                            subscription?.plan_id ?? ""
                        }
                        onChange={onChange}
                    >

                        {plans.map((plan) => (

                            <MenuItem
                                key={plan.plan_id}
                                value={plan.plan_id}
                            >
                                {plan.plan_name}
                            </MenuItem>

                        ))}

                    </TextField>

                    <Divider />

                    <Paper
                        variant="outlined"
                        sx={{
                            p: 3,
                            borderRadius: 2,
                            bgcolor: "grey.50",
                        }}
                    >

                        <Typography
                            variant="subtitle1"
                            fontWeight={700}
                            sx={{
                                mb: 2,
                            }}
                        >
                            Selected Plan
                        </Typography>

                        <Stack spacing={2}>

                            <Box
                                sx={{
                                    display: "flex",
                                    justifyContent: "space-between",
                                    alignItems: "center",
                                }}
                            >

                                <Typography
                                    color="text.secondary"
                                >
                                    Price
                                </Typography>

                                <Typography
                                    fontWeight={600}
                                >
                                    {selectedPlan
                                        ? `₦${Number(
                                            selectedPlan.price
                                        ).toLocaleString()}`
                                        : "--"}
                                </Typography>

                            </Box>

                            <Box
                                sx={{
                                    display: "flex",
                                    justifyContent: "space-between",
                                    alignItems: "center",
                                }}
                            >

                                <Typography
                                    color="text.secondary"
                                >
                                    Duration
                                </Typography>

                                <Typography
                                    fontWeight={600}
                                >
                                    {selectedPlan
                                        ? `${selectedPlan.duration_days} Days`
                                        : "--"}
                                </Typography>

                            </Box>

                            <Box
                                sx={{
                                    display: "flex",
                                    justifyContent: "space-between",
                                    alignItems: "center",
                                }}
                            >

                                <Typography
                                    color="text.secondary"
                                >
                                    Starts
                                </Typography>

                                <Typography
                                    fontWeight={600}
                                >
                                    Immediately
                                </Typography>

                            </Box>

                            <Box
                                sx={{
                                    display: "flex",
                                    justifyContent: "space-between",
                                    alignItems: "center",
                                }}
                            >

                                <Typography
                                    color="text.secondary"
                                >
                                    Expiry
                                </Typography>

                                <Typography
                                    fontWeight={600}
                                >
                                    Automatically Calculated
                                </Typography>

                            </Box>

                        </Stack>

                    </Paper>

                </Stack>

            </DialogContent>

            <DialogActions
                sx={{
                    px: 3,
                    pb: 3,
                }}
            >

                <Button
                    onClick={onClose}
                >
                    Cancel
                </Button>

                <Button
                    variant="contained"
                    onClick={onPurchase}
                    disabled={
                        !subscription?.customer_id ||
                        !subscription?.plan_id
                    }
                >
                    Purchase Subscription
                </Button>

            </DialogActions>

        </Dialog>

    );

}

export default SubscriptionPurchaseDialog;