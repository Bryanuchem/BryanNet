import {
    Button,
    Stack,
} from "@mui/material";

import RefreshIcon from "@mui/icons-material/Refresh";
import ClearIcon from "@mui/icons-material/Clear";

import FilterControl from "../common/FilterControl";

const REGISTRATION_OPTIONS = [
    {
        value: "all",
        label: "All",
    },
    {
        value: "registered",
        label: "Registered",
    },
    {
        value: "pending",
        label: "Pending",
    },
];

const STATUS_OPTIONS = [
    {
        value: "all",
        label: "All",
    },
    {
        value: "active",
        label: "Active",
    },
    {
        value: "inactive",
        label: "Inactive",
    },
];

function CustomerFilters({

    registration,

    status,

    onRegistrationChange,

    onStatusChange,

    onRefresh,

    onClear,

}) {

    return (

        <Stack
            direction="row"
            spacing={2}
            alignItems="center"
        >

            <FilterControl
                value={registration}
                placeholder="Registration"
                onChange={onRegistrationChange}
                options={REGISTRATION_OPTIONS}
                minWidth={160}
            />

            <FilterControl
                value={status}
                placeholder="Status"
                onChange={onStatusChange}
                options={STATUS_OPTIONS}
                minWidth={160}
            />

            <Button
                variant="outlined"
                startIcon={<RefreshIcon />}
                onClick={onRefresh}
                sx={{
                    height: 40,
                    whiteSpace: "nowrap",
                }}
            >
                Refresh
            </Button>

            <Button
                variant="outlined"
                startIcon={<ClearIcon />}
                color="inherit"
                onClick={onClear}
                sx={{
                    height: 40,
                    whiteSpace: "nowrap",
                }}
            >
                Clear
            </Button>

        </Stack>

    );

}

export default CustomerFilters;