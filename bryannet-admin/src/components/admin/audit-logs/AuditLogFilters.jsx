import RefreshIcon from "@mui/icons-material/Refresh";
import ClearIcon from "@mui/icons-material/Clear";

import {
    Button,
    Stack,
} from "@mui/material";

import SearchBar from "../../common/SearchBar";
import FilterControl from "../../common/FilterControl";
import ExportCsvButton from "../../common/ExportCsvButton";

import {
    useAdminUsers,
} from "../../../hooks/useAdminUsers";

function AuditLogFilters({

    filters,

    onFilterChange,

    onRefresh,

    onClear,

    auditLogs = [],

}) {

    const {

        data: administrators = [],

    } = useAdminUsers();

    const handleChange =

        (field) =>

        (event) => {

            onFilterChange(

                field,

                event.target.value,

            );

        };

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

                    value={filters.search}

                    onChange={(value) =>

                        onFilterChange(

                            "search",

                            value,

                        )

                    }

                    placeholder="Search audit logs..."

                    sx={{

                        flex: 1,

                    }}

                />

                <FilterControl

                    label="Action"

                    placeholder="All Actions"

                    value={filters.action}

                    onChange={

                        handleChange(

                            "action",

                        )

                    }

                    options={[

                        {

                            value: "",

                            label: "All Actions",

                        },

                        {

                            value: "LOGIN",

                            label: "Login",

                        },

                        {

                            value: "LOGOUT",

                            label: "Logout",

                        },

                        {

                            value: "CREATE",

                            label: "Create",

                        },

                        {

                            value: "UPDATE",

                            label: "Update",

                        },

                        {

                            value: "DELETE",

                            label: "Delete",

                        },

                        {

                            value: "ACTIVATE",

                            label: "Activate",

                        },

                        {

                            value: "DEACTIVATE",

                            label: "Deactivate",

                        },

                    ]}

                    minWidth={180}

                />

                <FilterControl

                    label="Administrator"

                    placeholder="All Administrators"

                    value={filters.admin_id}

                    onChange={

                        handleChange(

                            "admin_id",

                        )

                    }

                    options={[

                        {

                            value: "",

                            label: "All Administrators",

                        },

                        ...administrators.map(

                            (

                                administrator,

                            ) => ({

                                value:

                                    administrator.admin_user_id,

                                label:

                                    administrator.username,

                            }),

                        ),

                    ]}

                    minWidth={200}

                />

                <FilterControl

                    label="Result"

                    placeholder="All Results"

                    value={filters.result}

                    onChange={

                        handleChange(

                            "result",

                        )

                    }

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

                            value: "FAILED",

                            label: "Failed",

                        },

                        {

                            value: "WARNING",

                            label: "Warning",

                        },

                        {

                            value: "INFO",

                            label: "Info",

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

                    filename="audit-logs"

                    rows={auditLogs}

                />

            </Stack>

        </Stack>

    );
}

export default AuditLogFilters;