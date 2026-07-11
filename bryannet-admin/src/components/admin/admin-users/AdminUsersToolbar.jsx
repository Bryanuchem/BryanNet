import {
    Button,
    Stack,
} from "@mui/material";

import RefreshIcon from "@mui/icons-material/Refresh";
import ClearIcon from "@mui/icons-material/Clear";

import SearchBar from "../../common/SearchBar";
import FilterControl from "../../common/FilterControl";
import ExportCsvButton from "../../common/ExportCsvButton";

function AdminUsersToolbar({

    search,

    onSearchChange,

    role,

    onRoleChange,

    status,

    onStatusChange,

    roleOptions = [],

    administrators = [],

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

                    placeholder="Search username or email..."

                    sx={{

                        flex: 1,

                    }}

                />

                <FilterControl

                    label="Role"

                    placeholder="All Roles"

                    value={role}

                    onChange={onRoleChange}

                    options={[

                        {

                            value: "",

                            label: "All Roles",

                        },

                        ...roleOptions,

                    ]}

                    minWidth={180}

                />

                <FilterControl

                    label="Status"

                    placeholder="All Statuses"

                    value={status}

                    onChange={onStatusChange}

                    options={[

                        {

                            value: "",

                            label: "All Statuses",

                        },

                        {

                            value: true,

                            label: "Active",

                        },

                        {

                            value: false,

                            label: "Inactive",

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

                    filename="admin-users"

                    rows={administrators}

                />

            </Stack>

        </Stack>

    );

}

export default AdminUsersToolbar;