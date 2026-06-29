import {
    Stack,
} from "@mui/material";

import FilterControl from "../common/FilterControl";

import {
    useDashboardFilters,
} from "../../context/DashboardFiltersContext";

const YEAR_OPTIONS = [
    {
        value: 2026,
        label: "2026",
    },
    {
        value: 2025,
        label: "2025",
    },
    {
        value: 2024,
        label: "2024",
    },
];

const PERIOD_OPTIONS = [
    {
        value: "today",
        label: "Today",
    },
    {
        value: "7d",
        label: "Last 7 Days",
    },
    {
        value: "30d",
        label: "Last 30 Days",
    },
    {
        value: "month",
        label: "This Month",
    },
    {
        value: "quarter",
        label: "This Quarter",
    },
    {
        value: "year",
        label: "This Year",
    },
];

function DashboardFilters() {

    const {

        filters,

        updateFilters,

    } = useDashboardFilters();

    return (

        <Stack
            direction="row"
            spacing={2}
            justifyContent="flex-end"
            sx={{
                mb: 3,
            }}
        >

            <FilterControl
                value={filters.year}
                onChange={(event) =>
                    updateFilters({
                        year: Number(
                            event.target.value,
                        ),
                    })
                }
                options={YEAR_OPTIONS}
                minWidth={120}
            />

            <FilterControl
                value={filters.period}
                onChange={(event) =>
                    updateFilters({
                        period: event.target.value,
                    })
                }
                options={PERIOD_OPTIONS}
                minWidth={180}
            />

        </Stack>

    );

}

export default DashboardFilters;