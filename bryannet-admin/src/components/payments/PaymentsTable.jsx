import {
    Skeleton,
    Stack,
    Typography,
} from "@mui/material";

import {
    DataGrid,
} from "@mui/x-data-grid";

import {
    DeleteOutlineOutlined,
    EditOutlined,
    VisibilityOutlined,
} from "@mui/icons-material";

import {
    useMemo,
} from "react";

import DashboardSection from "../common/DashboardSection";
import ActionMenu from "../common/ActionMenu";
import BadgeChip from "../common/BadgeChip";

function PaymentsTable({

    payments = [],

    loading = false,

    onView,

    onEdit,

    onDelete,

}) {

    const columns = useMemo(

        () => [

            {

                field: "payment_reference",

                headerName: "Reference",

                flex: 1.3,

                minWidth: 220,

            },

            {

                field: "customer_name",

                headerName: "Customer",

                flex: 1.3,

                minWidth: 180,

            },

            {

                field: "amount",

                headerName: "Amount",

                width: 140,

                renderCell: (params) => (

                    <Typography
                        fontWeight={600}
                    >

                        ₦

                        {Number(
                            params.value ?? 0,
                        ).toLocaleString()}

                    </Typography>

                ),

            },

            {

                field: "payment_channel",

                headerName: "Channel",

                width: 140,

            },

            {

                field: "payment_method",

                headerName: "Method",

                width: 150,

                renderCell: (params) => (

                    params.value || "-"

                ),

            },

            {

                field: "status",

                headerName: "Status",

                width: 130,

                renderCell: (params) => (

                    <BadgeChip
                        status={params.value}
                    />

                ),

            },

            {

                field: "payment_date",

                headerName: "Payment Date",

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

                field: "actions",

                headerName: "",

                width: 70,

                sortable: false,

                filterable: false,

                disableColumnMenu: true,

                renderCell: (params) => (

                    <ActionMenu

                        items={[

                            {

                                label: "View",

                                icon: (

                                    <VisibilityOutlined
                                        fontSize="small"
                                    />

                                ),

                                onClick: () =>

                                    onView(
                                        params.row,
                                    ),

                            },

                            {

                                label: "Edit",

                                icon: (

                                    <EditOutlined
                                        fontSize="small"
                                    />

                                ),

                                onClick: () =>

                                    onEdit(
                                        params.row,
                                    ),

                            },

                            {

                                label: "Delete",

                                icon: (

                                    <DeleteOutlineOutlined
                                        fontSize="small"
                                    />

                                ),

                                onClick: () =>

                                    onDelete(
                                        params.row,
                                    ),

                            },

                        ]}

                    />

                ),

            },

        ],

        [

            onView,

            onEdit,

            onDelete,

        ],

    );

    return (

        <DashboardSection
            title="Payments"
        >

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

                    rows={payments}

                    columns={columns}

                    getRowId={(row) =>
                        row.payment_id
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

                    sx={{

                        border: 0,

                        "& .MuiDataGrid-columnHeaders": {

                            fontWeight: 700,

                            backgroundColor: "background.paper",

                        },

                        "& .MuiDataGrid-cell": {

                            display: "flex",

                            alignItems: "center",

                        },

                        "& .MuiDataGrid-footerContainer": {

                            borderTop: 1,

                            borderColor: "divider",

                        },

                        "& .MuiDataGrid-columnSeparator": {

                            display: "none",

                        },

                    }}

                />

            )}

        </DashboardSection>

    );

}

export default PaymentsTable;    