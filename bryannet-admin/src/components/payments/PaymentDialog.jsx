import {
    useEffect,
    useMemo,
    useState,
} from "react";

import {
    Autocomplete,
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
    usePlans,
} from "../../hooks/usePlans";

import {

    PAYMENT_CHANNEL_OPTIONS,

    PAYMENT_PROVIDER_OPTIONS,

    PaymentProvider,

} from "../../constants/payment";

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

    plan_id: null,

    payment_provider:
        PaymentProvider.MANUAL,

    payment_channel: "",

    payment_method: "",

};

function PaymentDialog({

    open,

    loading = false,

    onClose,

    onSubmit,

}) {

    const EMPTY_ARRAY = [];

    const {

        data: customersData,

        isLoading:
            customersLoading,

    } = useCustomers({

        page: 1,

        pageSize: 1000,

    });

    const {

        data: plansData,

        isLoading:
            plansLoading,

    } = usePlans({

        page: 1,

        pageSize: 100,

    });

    const customers =
        customersData ?? EMPTY_ARRAY;

    const plans =
        plansData?.items ?? EMPTY_ARRAY;

    const [

        form,

        setForm,

    ] = useState(
        DEFAULT_FORM,
    );

    useEffect(() => {

        if (

            open

        ) {

            setForm(
                DEFAULT_FORM,
            );

        }

    }, [

        open,

    ]);

    const filterCustomers = (
        options,
        { inputValue },
    ) => {

        const search =
            inputValue
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

        );

    };

    const selectedCustomer = useMemo(

        () =>

            customers.find(

                (customer) =>

                    customer.customer_id ===

                    form.customer_id,

            ) ?? null,

        [

            customers,

            form.customer_id,

        ],

    );

    const selectedPlan = useMemo(

        () =>

            plans.find(

                (plan) =>

                    plan.plan_id ===

                    form.plan_id,

            ) ?? null,

        [

            plans,

            form.plan_id,

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

        updateField(

            "customer_id",

            customer?.customer_id ?? null,

        );

    };

    const handlePlanChange = (

        _,

        plan,

    ) => {

        updateField(

            "plan_id",

            plan?.plan_id ?? null,

        );

    };

    const handleSubmit = () => {

        onSubmit(
            form,
        );

    };

    return (

        <FormDialog

            open={open}

            loading={loading}

            title="Record Payment"

            subtitle="Record a new customer payment."

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

                !form.plan_id ||

                !form.payment_channel

            }

            onSubmit={handleSubmit}

            onClose={onClose}

        >

            <FormSection

                title="Customer"

                subtitle="Select the customer making the payment."

            >

                <FormGrid>

                    <FormGridItem>

                        <Autocomplete

                            options={customers}

                            filterOptions={filterCustomers}

                            loading={customersLoading}

                            value={selectedCustomer}

                            onChange={handleCustomerChange}

                            isOptionEqualToValue={

                                (option, value) =>

                                    option.customer_id ===

                                    value.customer_id

                            }

                            getOptionLabel={(option) => {

                                return option.full_name ?? "";

                            }}

                        renderOption={(props, option) => {

                            const {
                                key,
                                ...optionProps
                            } = props;

                            return (

                                <li
                                    key={key}
                                    {...optionProps}
                                >

                                    <div>

                                        <Typography fontWeight={600}>
                                            {option.full_name}
                                        </Typography>

                                        <Typography
                                            variant="caption"
                                            color="text.secondary"
                                        >
                                            {option.phone_number}
                                        </Typography>

                                    </div>

                                </li>

                            );

                        }}

                            renderInput={(params) => (

                                <TextField

                                    {...params}

                                    label="Customer"

                                    placeholder="Search customer..."

                                />

                            )}
                        />

                    </FormGridItem>

                </FormGrid>

            </FormSection>

            <FormSection

                title="Subscription Plan"

                subtitle="Choose the plan being purchased."

            >

                <FormGrid>

                    <FormGridItem>

                        <Autocomplete

                            options={plans}

                            loading={plansLoading}

                            value={selectedPlan}

                            onChange={handlePlanChange}

                            isOptionEqualToValue={

                                (option, value) =>

                                    option.plan_id ===

                                    value.plan_id

                            }

                            getOptionLabel={(option) =>

                                option.plan_name ?? ""

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

                                            ₦

                                            {Number(

                                                option.price,

                                            ).toLocaleString()}

                                            {" • "}

                                            {option.duration_days} days

                                            {" • "}

                                            {option.speed_limit_mbps} Mbps

                                        </Typography>

                                    </div>

                                </li>

                            )}

                            renderInput={(params) => (

                                <TextField

                                    {...params}

                                    label="Plan"

                                    placeholder="Select a plan"

                                />

                            )}
                        />

                    </FormGridItem>

                </FormGrid>

            </FormSection>

            <FormSection

                title="Payment Information"

                subtitle="Enter how the payment was received."

                divider={false}

            >

                <FormGrid>

                    <FormGridItem md={6}>

                        <TextField

                            select

                            fullWidth

                            label="Payment Provider"

                            value={form.payment_provider}

                            onChange={(event) =>

                                updateField(

                                    "payment_provider",

                                    event.target.value,

                                )

                            }

                        >

                            {PAYMENT_PROVIDER_OPTIONS.map((provider) => (

                                <MenuItem
                                    key={provider.value}
                                    value={provider.value}
                                >

                                    {provider.label}

                                </MenuItem>

                            ))}

                        </TextField>

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
                            {PAYMENT_CHANNEL_OPTIONS.map((channel) => (

                                <MenuItem
                                    key={channel.value}
                                    value={channel.value}
                                >

                                    {channel.label}

                                </MenuItem>

                            ))}

                        </TextField>

                    </FormGridItem>

                    <FormGridItem>

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

                </FormGrid>

            </FormSection>

        </FormDialog>

    );

}

export default PaymentDialog;    