import {
    Button,
    Stack,
} from "@mui/material";

import RefreshIcon from "@mui/icons-material/Refresh";
import ClearIcon from "@mui/icons-material/Clear";
import DownloadIcon from "@mui/icons-material/Download";

import SearchBar from "../common/SearchBar";
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
        value: "pending",
        label: "Pending",
    },

    {
        value: "successful",
        label: "Successful",
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

    {
        value: "expired",
        label: "Expired",
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

    onExport,

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

                <SearchBar

                    value={search}

                    onChange={onSearchChange}

                    placeholder="Search customer, plan or payment reference..."

                    sx={{

                        flex: 1,

                    }}

                />

                <FilterControl

                    label="Channel"

                    placeholder="All Channels"

                    value={paymentChannel}

                    onChange={onPaymentChannelChange}

                    options={CHANNEL_OPTIONS}

                    minWidth={180}

                />

                <FilterControl

                    label="Status"

                    placeholder="All Statuses"

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

                <Button

                    variant="outlined"

                    startIcon={<DownloadIcon />}

                    onClick={onExport}
                >
                    Export CSV
                </Button>

            </Stack>

        </Stack>

    );

}

export default PaymentFilters;