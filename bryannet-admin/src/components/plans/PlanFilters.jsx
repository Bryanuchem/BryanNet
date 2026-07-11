import {
    Button,
    Stack,
} from "@mui/material";

import RefreshIcon from "@mui/icons-material/Refresh";
import ClearIcon from "@mui/icons-material/Clear";

import FilterControl from "../common/FilterControl";

const ACTIVE_OPTIONS = [
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

function PlanFilters({

    active,

    onActiveChange,

    onRefresh,

    onClear,

}) {

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
                    value={active}
                    placeholder="Status"
                    onChange={onActiveChange}
                    options={ACTIVE_OPTIONS}
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

            </Stack>

        </Stack>

    );

}

export default PlanFilters;