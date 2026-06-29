import {
    Button,
    Stack,
    TextField,
} from "@mui/material";

import RefreshIcon from "@mui/icons-material/Refresh";

import FilterControl from "../common/FilterControl";

const CHANNEL_OPTIONS = [
    {
        value: "",
        label: "All Channels",
    },
    {
        value: "Cash",
        label: "Cash",
    },
    {
        value: "Bank Transfer",
        label: "Bank Transfer",
    },
    {
        value: "POS",
        label: "POS",
    },
    {
        value: "Wallet",
        label: "Wallet",
    },
    {
        value: "Gateway",
        label: "Gateway",
    },
];

const STATUS_OPTIONS = [
    {
        value: "",
        label: "All Statuses",
    },
    {
        value: "successful",
        label: "Successful",
    },
    {
        value: "pending",
        label: "Pending",
    },
    {
        value: "failed",
        label: "Failed",
    },
    {
        value: "cancelled",
        label: "Cancelled",
    },
    {
        value: "refunded",
        label: "Refunded",
    },
];

function PaymentFilters({

    search,

    onSearchChange,

    paymentChannel,

    onPaymentChannelChange,

    status,

    onStatusChange,

    onRefresh,

    onClear,

}) {

    return (

        <Stack

            direction={{

                xs: "column",

                md: "row",

            }}

            spacing={2}

            alignItems="center"

            justifyContent="space-between"

            sx={{

                mb: 3,

            }}

        >

            <Stack

                direction={{

                    xs: "column",

                    sm: "row",

                }}

                spacing={2}

                sx={{

                    flex: 1,

                    width: "100%",

                }}

            >

                <TextField

                    size="small"

                    placeholder="Search customer, phone or reference..."

                    value={search}

                    onChange={(event) =>

                        onSearchChange(
                            event.target.value,
                        )

                    }

                    fullWidth

                />

                <FilterControl

                    value={paymentChannel}

                    onChange={onPaymentChannelChange}

                    options={CHANNEL_OPTIONS}

                    minWidth={180}

                />

                <FilterControl

                    value={status}

                    onChange={onStatusChange}

                    options={STATUS_OPTIONS}

                    minWidth={180}

                />

            </Stack>

            <Stack

                direction="row"

                spacing={1}

            >

                <Button

                    variant="outlined"

                    onClick={onClear}

                    disabled={!onClear}

                >

                    Clear

                </Button>

                <Button

                    variant="contained"

                    startIcon={<RefreshIcon />}

                    onClick={onRefresh}

                    disabled={!onRefresh}

                >

                    Refresh

                </Button>

            </Stack>

        </Stack>

    );

}

export default PaymentFilters;