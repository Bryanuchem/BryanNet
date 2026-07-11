import {
    Skeleton,
    Stack,
} from "@mui/material";

import {
    DataGrid,
} from "@mui/x-data-grid";

import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";

import {
    useMemo,
} from "react";

import {

    useCurrentPermissions,

} from "../../../hooks/useCurrentPermissions";

import EmptyState from "../../common/EmptyState";
import DashboardSection from "../../common/DashboardSection";
import ActionMenu from "../../common/ActionMenu";
import BadgeChip from "../../common/BadgeChip";

function SystemActivityTable({

    activities = [],

    loading = false,

    error = false,

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

                headerName: "Created",

                width: 180,

                renderCell: (params) => (

                    params.value

                        ? new Date(
                            params.value,
                        ).toLocaleString()

                        : "-"

                ),

            },

            {

                field: "action",

                headerName: "Action",

                width: 220,

                renderCell: (params) => (

                    params.value
                        ?.replaceAll(
                            "_",
                            " ",
                        )

                ),

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

                    />

                ),

            },

            {

                field: "target_name",

                headerName: "Target",

                width: 220,

                renderCell: (params) => (

                    params.value || "-"

                ),

            },

            {

                field: "description",

                headerName: "Description",

                flex: 1,

                minWidth: 320,

            },

            {

                field: "actions",

                headerName: "Actions",

                width: 80,

                sortable: false,

                filterable: false,

                disableColumnMenu: true,

                renderCell: (params) => {

                    const activity =

                        params.row;

                    const items = [];

                    if (

                        hasPermission(

                            "system_activity.view",

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

                                    activity,

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

        ],

    );

    if (error) {

        return (

            <DashboardSection>

                <EmptyState

                    title="Unable to load system activity"

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

            ) : activities.length === 0 ? (

                <EmptyState

                    title="No system activity recorded"

                    description={
                        "System events such as scheduled tasks, maintenance jobs and automation will appear here."
                    }

                />

            ) : (

                <DataGrid

                    autoHeight

                    rows={activities}

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

                                "system_activity.view",

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

                                    "system_activity.view",

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

export default SystemActivityTable;    