import {
    Skeleton,
    Stack,
} from "@mui/material";

import {
    DataGrid,
} from "@mui/x-data-grid";

import PersonOutlinedIcon from "@mui/icons-material/PersonOutlined";
import EditOutlinedIcon from "@mui/icons-material/EditOutlined";
import LockResetOutlinedIcon from "@mui/icons-material/LockResetOutlined";
import AdminPanelSettingsOutlinedIcon from "@mui/icons-material/AdminPanelSettingsOutlined";
import ToggleOnOutlinedIcon from "@mui/icons-material/ToggleOnOutlined";
import ToggleOffOutlinedIcon from "@mui/icons-material/ToggleOffOutlined";

import {
    useMemo,
} from "react";

import DashboardSection from "../../common/DashboardSection";
import ActionMenu from "../../common/ActionMenu";
import BadgeChip from "../../common/BadgeChip";

import {

    useCurrentPermissions,

} from "../../../hooks/useCurrentPermissions";

function AdminUsersTable({

    administrators = [],

    loading = false,

    onRowClick,

    onView,

    onEdit,

    onResetPassword,

    onChangeRole,

    onToggleStatus,

}) {

    const {

        hasPermission,

    } = useCurrentPermissions();

    const columns = useMemo(

        () => [

            {

                field: "username",

                headerName: "Username",

                flex: 1,

                minWidth: 170,

            },

            {

                field: "email",

                headerName: "Email",

                flex: 1.4,

                minWidth: 240,

            },

            {

                field: "role_name",

                headerName: "Role",

                width: 170,

            },

            {

                field: "is_active",

                headerName: "Status",

                width: 140,

                renderCell: (params) => (

                    <BadgeChip

                        status={

                            params.value

                                ? "active"

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

                field: "created_at",

                headerName: "Created",

                width: 180,

                renderCell: (params) => (

                    params.value

                        ? new Date(

                            params.value,

                        ).toLocaleDateString()

                        : "-"

                ),

            },

            {

                field: "actions",

                headerName: "Actions",

                width: 80,

                sortable: false,

                filterable: false,

                disableColumnMenu: true,

                renderCell: (params) => {

                    const administrator =

                        params.row;

                    const items = [];

                    // =====================================
                    // View
                    // =====================================

                    if (

                        hasPermission(

                            "admin_users.view",

                        )

                    ) {

                        items.push({

                            label: "View",

                            icon: (

                                <PersonOutlinedIcon

                                    fontSize="small"

                                />

                            ),

                            onClick: () =>

                                onView?.(

                                    administrator,

                                ),

                        });

                    }

                    // =====================================
                    // Edit
                    // =====================================

                    if (

                        hasPermission(

                            "admin_users.edit",

                        )

                    ) {

                        items.push({

                            label: "Edit",

                            icon: (

                                <EditOutlinedIcon

                                    fontSize="small"

                                />

                            ),

                            onClick: () =>

                                onEdit?.(

                                    administrator,

                                ),

                        });

                    }

                    // =====================================
                    // Change Role
                    // =====================================

                    if (

                        hasPermission(

                            "admin_users.change_role",

                        )

                    ) {

                        items.push({

                            label: "Change Role",

                            icon: (

                                <AdminPanelSettingsOutlinedIcon

                                    fontSize="small"

                                />

                            ),

                            onClick: () =>

                                onChangeRole?.(

                                    administrator,

                                ),

                        });

                    }

                    // =====================================
                    // Reset Password
                    // =====================================

                    if (

                        hasPermission(

                            "admin_users.reset_password",

                        )

                    ) {

                        items.push({

                            label: "Reset Password",

                            icon: (

                                <LockResetOutlinedIcon

                                    fontSize="small"

                                />

                            ),

                            onClick: () =>

                                onResetPassword?.(

                                    administrator,

                                ),

                        });

                    }

                    // =====================================
                    // Activate / Deactivate
                    // =====================================

                    if (

                        administrator.is_active

                            ? hasPermission(

                                "admin_users.deactivate",

                            )

                            : hasPermission(

                                "admin_users.activate",

                            )

                    ) {

                        items.push({

                            label:

                                administrator.is_active

                                    ? "Deactivate"

                                    : "Activate",

                            icon:

                                administrator.is_active

                                    ? (

                                        <ToggleOffOutlinedIcon

                                            fontSize="small"

                                        />

                                    )

                                    : (

                                        <ToggleOnOutlinedIcon

                                            fontSize="small"

                                        />

                                    ),

                            onClick: () =>

                                onToggleStatus?.(

                                    administrator,

                                ),

                        });

                    }

                    return (

                        <div

                            onClick={(event) => {

                                event.stopPropagation();

                            }}

                        >

                            <ActionMenu

                                items={items}

                            />

                        </div>

                    );

                },

            },

        ],

        [

            hasPermission,

            onView,

            onEdit,

            onResetPassword,

            onChangeRole,

            onToggleStatus,

        ],

    );

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

            ) : (

                <DataGrid

                    autoHeight

                    rows={administrators}

                    columns={columns}

                    getRowId={(row) =>

                        row.admin_user_id

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

                                "admin_users.view",

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

                            cursor: hasPermission(

                                "admin_users.view",

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

                            outline:

                                "none !important",

                        },

                    }}

                />

            )}

        </DashboardSection>

    );

}

export default AdminUsersTable;        