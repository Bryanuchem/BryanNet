import {
    Button,
    Stack,
} from "@mui/material";

import RefreshIcon from "@mui/icons-material/Refresh";
import ClearIcon from "@mui/icons-material/Clear";

import FilterControl from "../common/FilterControl";

const STATUS_OPTIONS = [
    {
        value: "all",
        label: "All Statuses",
    },
    {
        value: "active",
        label: "Active",
    },
    {
        value: "inactive",
        label: "Inactive",
    },
    {
        value: "blocked",
        label: "Blocked",
    },
];

function DeviceFilters({

    status,

    onStatusChange,

    onRefresh,

    onClear,

}) {

    return (

        <Stack
            direction="row"
            spacing={2}
        >

            <FilterControl
                value={status}
                placeholder="Status"
                onChange={onStatusChange}
                options={STATUS_OPTIONS}
                minWidth={180}
            />

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

    );

}

export default DeviceFilters;