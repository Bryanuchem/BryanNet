import {
    Skeleton,
    Stack,
} from "@mui/material";

import {
    DataGrid,
} from "@mui/x-data-grid";

import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";
import BlockOutlinedIcon from "@mui/icons-material/BlockOutlined";

import {
    useMemo,
} from "react";

import {

    useCurrentPermissions,

} from "../../../hooks/useCurrentPermissions";


import DashboardSection from "../../common/DashboardSection";
import ActionMenu from "../../common/ActionMenu";
import BadgeChip from "../../common/BadgeChip";
import EmptyState from "../../common/EmptyState";

function LoginSessionsTable({

    sessions = [],

    loading = false,

    error = false,

    onRowClick,

    onView,

    onRevoke,

}) {

    const {

        hasPermission,

    } = useCurrentPermissions();

    const columns = useMemo(

        () => [

            {

                field: "login_time",

                headerName: "Login Time",

                width: 190,

                renderCell: (params) => (

                    params.value

                        ? new Date(

                            params.value,

                        ).toLocaleString()

                        : "-"

                ),

            },

            {

                field: "administrator",

                headerName: "Administrator",

                flex: 1,

                width: 180,

            },

            {

                field: "client_name",

                flex: 1,

                headerName: "Device",

                width: 170,

            },

            {

                field: "login_source",

                headerName: "Browser",

                width: 120,

            },

            {

                field: "ip_address",

                headerName: "IP Address",

                width: 170,

                renderCell: (params) => (

                    params.value || "-"

                ),

            },

            {

                field: "is_active",

                headerName: "Status",

                width: 120,

                renderCell: (params) => (

                    <BadgeChip

                        status={

                            params.value

                                ? "success"

                                : "inactive"

                        }

                        label={

                            params.value

                                ? "Active"

                                : "Inactive"

                        }

                    />

                ),

            },

            {

                field: "actions",

                headerName: "Actions",

                width: 90,

                sortable: false,

                filterable: false,

                disableColumnMenu: true,

                renderCell: (params) => {

                    const session =

                        params.row;

                    const items = [];

                    if (

                        hasPermission(

                            "login_sessions.view",

                        )

                    ) {

                        items.push({

                            label: "View Details",

                            icon: (

                                <VisibilityOutlinedIcon

                                    fontSize="small"

                                />

                            ),

                            onClick: () =>

                                onView?.(

                                    session,

                                ),

                        });

                    }

                    if (

                        session.is_active &&

                        hasPermission(

                            "login_sessions.revoke",

                        )

                    ) {

                        items.push({

                            label: "Revoke Session",

                            icon: (

                                <BlockOutlinedIcon

                                    fontSize="small"

                                />

                            ),

                            onClick: () =>

                                onRevoke?.(

                                    session,

                                ),

                        });

                    }

                    return items.length > 0 ? (

                        <ActionMenu

                            items={items}

                        />

                    ) : null;

                },

            },

        ],

        [

            hasPermission,

            onView,

            onRevoke,

        ]

    );

    if (error) {

        return (

            <DashboardSection>

                <EmptyState

                    title="Unable to load login sessions"

                    description="Please try refreshing the page."

                />

            </DashboardSection>

        );

    }

    return (

        <DashboardSection>

            {loading ? (

                <Stack
                    spacing={2}
                >

                    {[...Array(8)].map(

                        (_, index) => (

                            <Skeleton

                                key={index}

                                variant="rounded"

                                height={52}

                            />

                        ),

                    )}

                </Stack>

            ) : sessions.length === 0 ? (

                <EmptyState

                    title="No login sessions found"

                    description={
                        "Administrator login sessions will appear here."
                    }

                />

            ) : (

                <DataGrid

                    autoHeight

                    rows={sessions}

                    columns={columns}

                    getRowId={(row) =>

                        row.admin_session_id

                    }

                    disableRowSelectionOnClick

                    pageSizeOptions={[

                        10,

                        25,

                        50,

                    ]}

                    initialState={{

                        pagination: {

                            paginationModel: {

                                pageSize: 10,

                            },

                        },

                    }}

                    onRowClick={(params) => {

                        if (

                            hasPermission(

                                "login_sessions.view",

                            )

                        ) {

                            onRowClick?.(

                                params.row,

                            );

                        }

                    }}

                    sx={{

                        border: 0,

                        "& .MuiDataGrid-columnHeaders": {

                            fontWeight: 700,

                            backgroundColor:
                                "background.paper",

                        },

                        "& .MuiDataGrid-columnSeparator": {

                            display: "none",

                        },

                        "& .MuiDataGrid-cell": {

                            display: "flex",

                            alignItems: "center",

                            "&:focus": {

                                outline: "none",

                            },

                            "&:focus-within": {

                                outline: "none",

                            },

                        },

                        "& .MuiDataGrid-row": {

                            cursor:

                                hasPermission(

                                    "login_sessions.view",

                                )

                                    ? "pointer"

                                    : "default",

                        },

                        "& .MuiDataGrid-row:nth-of-type(odd)": {

                            backgroundColor:
                                "action.hover",

                        },

                        "& .MuiDataGrid-footerContainer": {

                            borderTop: 1,

                            borderColor:
                                "divider",

                        },

                    }}

                />

            )}

        </DashboardSection>

    );

}

export default LoginSessionsTable;    