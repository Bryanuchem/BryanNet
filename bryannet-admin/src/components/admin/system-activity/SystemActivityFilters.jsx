import {
    Button,
    Stack,
} from "@mui/material";

import RefreshIcon from "@mui/icons-material/Refresh";
import ClearIcon from "@mui/icons-material/Clear";

import SearchBar from "../../common/SearchBar";
import FilterControl from "../../common/FilterControl";
import ExportCsvButton from "../../common/ExportCsvButton";

function SystemActivityFilters({

    search,

    onSearchChange,

    action,

    onActionChange,

    result,

    onResultChange,

    activities = [],

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

                <SearchBar

                    value={search}

                    onChange={onSearchChange}

                    placeholder="Search system activity..."

                    sx={{

                        flex: 1,

                    }}

                />

                <FilterControl

                    label="Action"

                    placeholder="All Actions"

                    value={action}

                    onChange={onActionChange}

                    options={[

                        {

                            value: "",

                            label: "All Actions",

                        },

                        {

                            value: "AUTOMATION_RUN_ALL",

                            label: "Run All",

                        },

                        {

                            value: "AUTOMATION_PAYMENTS",

                            label: "Payment Maintenance",

                        },

                        {

                            value: "AUTOMATION_SUBSCRIPTIONS",

                            label: "Subscription Maintenance",

                        },

                        {

                            value: "AUTOMATION_DEVICES",

                            label: "Router Maintenance",

                        },

                        {

                            value: "AUTOMATION_REMINDERS",

                            label: "Notification Scheduler",

                        },

                    ]}
                    
                    minWidth={220}

                />

                <FilterControl

                    label="Result"

                    placeholder="All Results"

                    value={result}

                    onChange={onResultChange}

                    options={[

                        {

                            value: "",

                            label: "All Results",

                        },

                        {

                            value: "SUCCESS",

                            label: "Success",

                        },

                        {

                            value: "WARNING",

                            label: "Warning",

                        },

                        {

                            value: "INFO",

                            label: "Info",

                        },

                        {

                            value: "FAILED",

                            label: "Failed",

                        },

                    ]}

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

                <ExportCsvButton

                    filename="system-activity"

                    rows={activities}

                />

            </Stack>

        </Stack>

    );

}

export default SystemActivityFilters;