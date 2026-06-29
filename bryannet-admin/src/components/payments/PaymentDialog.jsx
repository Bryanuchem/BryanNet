import {
    useEffect,
    useMemo,
    useState,
} from "react";

import {
    Autocomplete,
    CircularProgress,
    InputAdornment,
    MenuItem,
    TextField,
    Typography,
} from "@mui/material";

import PaymentsRoundedIcon from "@mui/icons-material/PaymentsRounded";

import FormDialog from "../common/FormDialog";
import FormSection from "../common/FormSection";
import FormGrid from "../common/FormGrid";
import FormGridItem from "../common/FormGridItem";

import {
    useCustomers,
} from "../../hooks/useCustomers";

import {
    useSubscriptions,
} from "../../hooks/useSubscriptions";

const PAYMENT_CHANNELS = [
    "Cash",
    "Bank Transfer",
    "POS",
    "Wallet",
    "Gateway",
];

const PAYMENT_METHODS = [
    "Opay",
    "Moniepoint",
    "PalmPay",
    "Paystack",
    "Flutterwave",
    "GTBank",
    "Access Bank",
    "UBA",
    "First Bank",
    "Zenith Bank",
];

const DEFAULT_FORM = {

    customer_id: null,

    subscription_id: null,

    amount: "",

    payment_channel: "",

    payment_method: "",

    status: "successful",

    payment_date: new Date()
        .toISOString()
        .slice(0, 16),

    notes: "",

};

function PaymentDialog({

    open,

    loading = false,

    initialValues = null,

    onClose,

    onSubmit,

}) {

    const {

        data: customers = [],

        isLoading: customersLoading,

    } = useCustomers();

    const {

        data: subscriptions = [],

        isLoading: subscriptionsLoading,

    } = useSubscriptions();

    const [

        form,

        setForm,

    ] = useState(DEFAULT_FORM);

    useEffect(() => {

        if (!open) {

            return;

        }

        setForm(

            initialValues

                ? {

                    ...DEFAULT_FORM,

                    ...initialValues,

                }

                : DEFAULT_FORM,

        );

    }, [

        open,

        initialValues,

    ]);

    const selectedCustomer = useMemo(

        () =>

            customers.find(

                (customer) =>

                    customer.customer_id ===
                    form.customer_id,

            ) || null,

        [

            customers,

            form.customer_id,

        ],

    );

    const availableSubscriptions = useMemo(

        () =>

            subscriptions.filter(

                (subscription) =>

                    subscription.customer_id ===
                    form.customer_id,

            ),

        [

            subscriptions,

            form.customer_id,

        ],

    );

    const selectedSubscription = useMemo(

        () =>

            availableSubscriptions.find(

                (subscription) =>

                    subscription.subscription_id ===
                    form.subscription_id,

            ) || null,

        [

            availableSubscriptions,

            form.subscription_id,

        ],

    );

    const updateField = (

        field,

        value,

    ) => {

        setForm(

            (previous) => ({

                ...previous,

                [field]: value,

            }),

        );

    };

    const handleCustomerChange = (

        _,

        customer,

    ) => {

        setForm(

            (previous) => ({

                ...previous,

                customer_id:

                    customer?.customer_id ?? null,

                subscription_id: null,

            }),

        );

    };

    const handleSubscriptionChange = (

        _,

        subscription,

    ) => {

        updateField(

            "subscription_id",

            subscription?.subscription_id ?? null,

        );

    };

    const handleSubmit = () => {

        onSubmit(form);

    };

    return (

        <FormDialog

            open={open}

            loading={loading}

            title="Record Payment"

            subtitle="Record a payment received from a customer."

            icon={

                <PaymentsRoundedIcon

                    color="primary"

                    fontSize="large"

                />

            }

            maxWidth="md"

            submitText="Record Payment"

            loadingText="Recording..."

            disableSubmit={

                !form.customer_id ||

                !form.amount ||

                !form.payment_channel

            }

            onSubmit={handleSubmit}

            onClose={onClose}

        >

            <FormSection

                title="Customer Information"

                subtitle="Choose the customer and subscription."

            >

                <FormGrid>

                    <FormGridItem>

                        <Autocomplete

                            options={customers}

                            loading={customersLoading}

                            value={selectedCustomer}

                            onChange={handleCustomerChange}

                            isOptionEqualToValue={

                                (option, value) =>

                                    option.customer_id ===
                                    value.customer_id

                            }

                            getOptionLabel={(option) =>

                                option.full_name || ""

                            }

                            renderOption={(props, option) => (

                                <li {...props}>

                                    <div>

                                        <Typography
                                            fontWeight={600}
                                        >

                                            {option.full_name}

                                        </Typography>

                                        <Typography
                                            variant="caption"
                                            color="text.secondary"
                                        >

                                            📞 {option.phone_number}

                                        </Typography>

                                        <br />

                                        <Typography
                                            variant="caption"
                                            color="text.secondary"
                                        >

                                            Customer #

                                            {option.customer_id}

                                        </Typography>

                                    </div>

                                </li>

                            )}

                            renderInput={(params) => (

                                <TextField

                                    {...params}

                                    label="Customer"

                                    placeholder="Search customer..."

                                    InputProps={{

                                        ...params.InputProps,

                                        endAdornment: (

                                            <>

                                                {customersLoading && (

                                                    <CircularProgress
                                                        size={18}
                                                    />

                                                )}

                                                {

                                                    params.InputProps.endAdornment

                                                }

                                            </>

                                        ),

                                    }}

                                />

                            )}

                        />

                    </FormGridItem>

                    <FormGridItem>

                        <Autocomplete

                            options={availableSubscriptions}

                            loading={subscriptionsLoading}

                            disabled={!form.customer_id}

                            value={selectedSubscription}

                            onChange={handleSubscriptionChange}

                            isOptionEqualToValue={

                                (option, value) =>

                                    option.subscription_id ===
                                    value.subscription_id

                            }

                            getOptionLabel={(option) =>

                                option.plan_name ||
                                `Subscription #${option.subscription_id}`

                            }

                            renderOption={(props, option) => (

                                <li {...props}>

                                    <div>

                                        <Typography
                                            fontWeight={600}
                                        >

                                            {option.plan_name}

                                        </Typography>

                                        <Typography
                                            variant="caption"
                                            color="text.secondary"
                                        >

                                            {option.status}

                                        </Typography>

                                        <br />

                                        <Typography
                                            variant="caption"
                                            color="text.secondary"
                                        >

                                            Expires{" "}

                                            {new Date(
                                                option.expiry_date,
                                            ).toLocaleDateString()}

                                        </Typography>

                                    </div>

                                </li>

                            )}

                            renderInput={(params) => (

                                <TextField

                                    {...params}

                                    label="Subscription"

                                    placeholder="Select subscription"

                                />

                            )}

                        />

                    </FormGridItem>

                </FormGrid>

            </FormSection>

            <FormSection
                title="Payment Details"
                subtitle="Enter the payment information."
            >

                <FormGrid>

                    <FormGridItem md={6}>

                        <TextField

                            fullWidth

                            type="number"

                            label="Amount"

                            value={form.amount}

                            onChange={(event) =>

                                updateField(
                                    "amount",
                                    event.target.value,
                                )

                            }

                            slotProps={{

                                input: {

                                    startAdornment: (

                                        <InputAdornment position="start">

                                            ₦

                                        </InputAdornment>

                                    ),

                                },

                            }}

                        />

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <TextField

                            select

                            fullWidth

                            label="Payment Channel"

                            value={form.payment_channel}

                            onChange={(event) =>

                                updateField(
                                    "payment_channel",
                                    event.target.value,
                                )

                            }

                        >

                            {PAYMENT_CHANNELS.map((channel) => (

                                <MenuItem
                                    key={channel}
                                    value={channel}
                                >

                                    {channel}

                                </MenuItem>

                            ))}

                        </TextField>

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <Autocomplete

                            freeSolo

                            options={PAYMENT_METHODS}

                            value={form.payment_method}

                            onInputChange={(_, value) =>

                                updateField(
                                    "payment_method",
                                    value,
                                )

                            }

                            renderInput={(params) => (

                                <TextField

                                    {...params}

                                    label="Payment Method"

                                    placeholder="Select or type a payment method"

                                />

                            )}

                        />

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <TextField

                            select

                            fullWidth

                            label="Status"

                            value={form.status}

                            onChange={(event) =>

                                updateField(
                                    "status",
                                    event.target.value,
                                )

                            }

                        >

                            <MenuItem value="successful">

                                🟢 Successful

                            </MenuItem>

                            <MenuItem value="pending">

                                🟡 Pending

                            </MenuItem>

                            <MenuItem value="failed">

                                🔴 Failed

                            </MenuItem>

                            <MenuItem value="cancelled">

                                ⚫ Cancelled

                            </MenuItem>

                            <MenuItem value="refunded">

                                🔵 Refunded

                            </MenuItem>

                        </TextField>

                    </FormGridItem>

                    <FormGridItem>

                        <TextField

                            fullWidth

                            type="datetime-local"

                            label="Payment Date"

                            value={form.payment_date}

                            onChange={(event) =>

                                updateField(
                                    "payment_date",
                                    event.target.value,
                                )

                            }

                            slotProps={{

                                inputLabel: {

                                    shrink: true,

                                },

                            }}

                        />

                    </FormGridItem>

                </FormGrid>

            </FormSection>

            <FormSection

                title="Additional Information"

                subtitle="Optional information for future reference."

                divider={false}

            >

                <TextField

                    fullWidth

                    multiline

                    rows={4}

                    label="Notes"

                    placeholder="Enter any notes about this payment..."

                    value={form.notes}

                    onChange={(event) =>

                        updateField(
                            "notes",
                            event.target.value,
                        )

                    }

                />

            </FormSection>

        </FormDialog>

    );

}

export default PaymentDialog;            