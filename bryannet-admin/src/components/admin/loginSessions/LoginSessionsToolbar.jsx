import {
    Button,
    Stack,
} from "@mui/material";

import RefreshIcon from "@mui/icons-material/Refresh";
import ClearIcon from "@mui/icons-material/Clear";

import SearchBar from "../../common/SearchBar";
import FilterControl from "../../common/FilterControl";
import ExportCsvButton from "../../common/ExportCsvButton";

function LoginSessionsToolbar({

    search,

    onSearchChange,

    status,

    onStatusChange,

    browser,

    onBrowserChange,

    sessions = [],

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

                    onChange={(event) =>

                        onSearchChange(

                            event.target.value,

                        )

                    }

                    placeholder="Search login sessions..."

                    sx={{

                        flex: 1,

                    }}

                />

                <FilterControl

                    placeholder="All Statuses"

                    value={status}

                    onChange={(event) =>

                        onStatusChange(

                            event.target.value,

                        )

                    }

                    options={[

                        {

                            value: "",

                            label: "All Statuses",

                        },

                        {

                            value: "true",

                            label: "Active",

                        },

                        {

                            value: "false",

                            label: "Inactive",

                        },

                    ]}

                    minWidth={180}

                />

                <FilterControl

                    placeholder="All Browsers"

                    value={browser}

                    onChange={(event) =>

                        onBrowserChange(

                            event.target.value,

                        )

                    }

                    options={[

                        {

                            value: "",

                            label: "All Browsers",

                        },

                        {

                            value: "WEB",

                            label: "Web",

                        },

                        {

                            value: "MOBILE",

                            label: "Mobile",

                        },

                        {

                            value: "API",

                            label: "API",

                        },

                    ]}

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

                <ExportCsvButton

                    filename="login-sessions"

                    rows={sessions}

                />

            </Stack>

        </Stack>

    );

}

export default LoginSessionsToolbar;