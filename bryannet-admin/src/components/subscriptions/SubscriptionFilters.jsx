import {
    Button,
    Stack,
} from "@mui/material";

import RefreshIcon from "@mui/icons-material/Refresh";
import ClearIcon from "@mui/icons-material/Clear";

import FilterControl from "../common/FilterControl";

function SubscriptionFilters({

    customers,

    plans,

    customerId,

    planId,

    status,

    onCustomerChange,

    onPlanChange,

    onStatusChange,

    onRefresh,

    onClear,

}) {

    const customerOptions = [

        {

            value: "",

            label: "All Customers",

        },

        ...customers.map((customer) => ({

            value: customer.customer_id,

            label: customer.full_name,

        })),

    ];

    const planOptions = [

        {

            value: "",

            label: "All Plans",

        },

        ...plans.map((plan) => ({

            value: plan.plan_id,

            label: plan.plan_name,

        })),

    ];

    const statusOptions = [

        {

            value: "",

            label: "All Statuses",

        },

        {

            value: "active",

            label: "Active",

        },

        {

            value: "expired",

            label: "Expired",

        },

        {

            value: "cancelled",

            label: "Cancelled",

        },

        {

            value: "pending",

            label: "Pending",

        },

    ];

    return (

        <Stack

            direction="row"

            spacing={2}

            justifyContent="space-between"

            alignItems="center"

        >

            <Stack

                direction="row"

                spacing={2}

            >

                <FilterControl

                    value={customerId}

                    placeholder="Customer"

                    onChange={onCustomerChange}

                    options={customerOptions}

                    minWidth={220}

                />

                <FilterControl

                    value={planId}

                    placeholder="Plan"

                    onChange={onPlanChange}

                    options={planOptions}

                    minWidth={180}

                />

                <FilterControl

                    value={status}

                    placeholder="Status"

                    onChange={onStatusChange}

                    options={statusOptions}

                    minWidth={170}

                />

            </Stack>

            <Stack

                direction="row"

                spacing={1}

            >

                <Button

                    variant="outlined"

                    startIcon={<RefreshIcon />}

                    onClick={onRefresh}

                >

                    Refresh

                </Button>

                <Button

                    variant="outlined"

                    color="inherit"

                    startIcon={<ClearIcon />}

                    onClick={onClear}

                >

                    Clear

                </Button>

            </Stack>

        </Stack>

    );

}

export default SubscriptionFilters;