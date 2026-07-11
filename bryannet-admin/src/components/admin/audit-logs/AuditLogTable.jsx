import {
    Skeleton,
    Stack,
    Typography,
} from "@mui/material";

import {
    DataGrid,
} from "@mui/x-data-grid";

import {
    useMemo,
} from "react";

import {

    useCurrentPermissions,

} from "../../../hooks/useCurrentPermissions";

import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";

import ActionMenu from "../../common/ActionMenu";

import DashboardSection from "../../common/DashboardSection";
import BadgeChip from "../../common/BadgeChip";

function AuditLogTable({

    auditLogs = [],

    loading = false,

    onRowClick,

    onView,

}) {

    const {

        hasPermission,

    } = useCurrentPermissions();

    const columns = useMemo(

        () => [

            {

                field: "created_at",

                headerName: "Timestamp",

                width: 180,

                renderCell: (params) =>

                    params.value

                        ? new Date(

                            params.value,

                        ).toLocaleString()

                        : "-",

            },

            {

                field: "administrator",

                headerName: "Administrator",

                flex: 1,

                minWidth: 170,

            },

            {

                field: "action",

                headerName: "Action",

                width: 170,

            },

            {

                field: "entity_type",

                headerName: "Entity",

                width: 170,

            },

            {

                field: "target_name",

                headerName: "Target",

                flex: 1,

                minWidth: 170,

                renderCell: (params) =>

                    params.value || "-",

            },

            {

                field: "result",

                headerName: "Result",

                width: 140,

                renderCell: (params) => (

                    <BadgeChip

                        status={

                            params.value

                                ?.toLowerCase()

                        }

                        label={

                            params.value

                        }

                    />

                ),

            },

            {

                field: "description",

                headerName: "Description",

                flex: 1.5,

                minWidth: 260,

                renderCell: (params) => (

                    <Typography

                        variant="body2"

                        noWrap

                        sx={{

                            width: "100%",

                        }}

                    >

                        {

                            params.value

                        }

                    </Typography>

                ),

            },

            {

                field: "actions",

                headerName: "Actions",

                width: 80,

                sortable: false,

                filterable: false,

                disableColumnMenu: true,

                renderCell: (params) => (

                    <div

                        onClick={(event) => {

                            event.stopPropagation();

                        }}

                    >

                        <ActionMenu

                            items={

                                hasPermission(

                                    "audit_logs.view",

                                )

                                    ? [

                                        {

                                            label: "View Details",

                                            icon: (

                                                <VisibilityOutlinedIcon

                                                    fontSize="small"

                                                />

                                            ),

                                            onClick: () =>

                                                onView?.(

                                                    params.row,

                                                ),

                                        },

                                    ]

                                    : []

                            }
                        />

                    </div>

                ),

            },

        ],

        [

            hasPermission,

            onView,

        ],

    );

    if (loading) {

        return (

            <DashboardSection>

                <Stack spacing={2}>

                    {[...Array(8)].map((_, index) => (

                        <Skeleton

                            key={index}

                            variant="rounded"

                            height={52}

                        />

                    ))}

                </Stack>

            </DashboardSection>

        );

    }

    return (

        <DashboardSection>

            <DataGrid

                autoHeight

                rows={auditLogs}

                columns={columns}

                getRowId={(row) =>

                    row.audit_log_id

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

                            "audit_logs.view",

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

                    },

                    "& .MuiDataGrid-row": {

                        cursor:

                            hasPermission(

                                "audit_logs.view",

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

                    "& .MuiDataGrid-cell:focus, \
& .MuiDataGrid-cell:focus-within, \
& .MuiDataGrid-columnHeader:focus, \
& .MuiDataGrid-columnHeader:focus-within": {

                        outline: "none !important",

                    },

                }}

            />

        </DashboardSection>

    );

}

export default AuditLogTable;            