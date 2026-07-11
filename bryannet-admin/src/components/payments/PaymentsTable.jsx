import {
    Skeleton,
    Stack,
    Typography,
} from "@mui/material";

import {
    DataGrid,
} from "@mui/x-data-grid";

import ReceiptLongOutlinedIcon from "@mui/icons-material/ReceiptLongOutlined";
import MoneyOffOutlinedIcon from "@mui/icons-material/MoneyOffOutlined";
import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";
import PriceCheckOutlinedIcon from "@mui/icons-material/PriceCheckOutlined";
import RemoveDoneOutlinedIcon from "@mui/icons-material/RemoveDoneOutlined";
import ScheduleIcon from "@mui/icons-material/Schedule";


import {
    useMemo,
} from "react";

import DashboardSection from "../common/DashboardSection";
import ActionMenu from "../common/ActionMenu";
import BadgeChip from "../common/BadgeChip";

import {
    useCurrentPermissions,
} from "../../hooks/useCurrentPermissions";

function PaymentsTable({

    payments = [],

    loading = false,

    page,

    rowsPerPage,

    total,

    onPageChange,

    onRowsPerPageChange,

    onView,

    onRowClick,


    onPrintReceipt,

    onComplete,

    onRefund,

    onCancel,

    onExpire,

}) {

    const {

        hasPermission,

    } = useCurrentPermissions();

    const columns = useMemo(

        () => [

            {

                field: "payment_reference",

                headerName: "Reference",

                flex: 1.35,

                minWidth: 220,

            },

            {

                field: "customer_name",

                headerName: "Customer",

                flex: 1.25,

                minWidth: 180,

            },

            {

                field: "plan_name",

                headerName: "Plan",

                width: 170,

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

                width: 140,

                renderCell: (params) => (

                    <BadgeChip
                        status={params.value}
                    />

                ),

            },

            {

                field: "payment_date",

                headerName: "Payment Date",

                width: 185,

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

                headerName: "Actions",

                align: "center",

                headerAlign: "center",

                width: 70,

                sortable: false,

                filterable: false,

                disableColumnMenu: true,

                renderCell: (params) => {

                    const payment = params.row;

                    const items = [];

                    if (

                        hasPermission(

                            "payments.view",

                        )

                    ) {

                        items.push({

                            label: "View",

                            icon: (

                                <VisibilityOutlinedIcon

                                    fontSize="small"

                                />

                            ),

                            onClick: () =>

                                onView(

                                    payment,

                                ),

                        });

                    }

                    if (

                        payment.status === "successful"

                    ) {

                        if (

                            hasPermission(

                                "payments.view",

                            )

                        ) {

                            items.push({

                                label: "Print Receipt",

                                icon: (

                                    <ReceiptLongOutlinedIcon

                                        fontSize="small"

                                    />

                                ),

                                onClick: () =>

                                    onPrintReceipt(

                                        payment,

                                    ),

                            });

                        }

                        if (

                            hasPermission(

                                "payments.refund",

                            )

                        ) {

                            items.push({

                                label: "Refund",

                                icon: (

                                    <MoneyOffOutlinedIcon

                                        fontSize="small"

                                    />

                                ),

                                onClick: () =>

                                    onRefund(

                                        payment,

                                    ),

                            });

                        }

                    }

                    if (

                        payment.status === "pending"

                    ) {

                        if (

                            hasPermission(

                                "payments.complete",

                            )

                        ) {

                            items.push({

                                label: "Complete",

                                icon: (

                                    <PriceCheckOutlinedIcon

                                        fontSize="small"

                                    />

                                ),

                                onClick: () =>

                                    onComplete(

                                        payment,

                                    ),

                            });

                        }

                        if (

                            hasPermission(

                                "payments.cancel",

                            )

                        ) {

                            items.push({

                                label: "Cancel",

                                icon: (

                                    <RemoveDoneOutlinedIcon

                                        fontSize="small"

                                    />

                                ),

                                onClick: () =>

                                    onCancel(

                                        payment,

                                    ),

                            });

                        }

                        if (

                            hasPermission(

                                "payments.expire",

                            )

                        ) {

                            items.push({

                                label: "Expire",

                                icon: (

                                    <ScheduleIcon

                                        fontSize="small"

                                    />

                                ),

                                onClick: () =>

                                    onExpire(

                                        payment,

                                    ),

                            });

                        }

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

            onPrintReceipt,

            onComplete,

            onRefund,

            onCancel,

            onExpire,

        ],

    );

    return (

        <DashboardSection
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
                        row.payment_reference
                    }

                    disableRowSelectionOnClick

                    paginationMode="server"

                    rowCount={total}

                    paginationModel={{

                        page,

                        pageSize:
                            rowsPerPage,

                    }}

                    onPaginationModelChange={(model) => {

                        if (
                            model.page !== page
                        ) {

                            onPageChange(
                                null,
                                model.page,
                            );

                        }

                        if (

                            model.pageSize
                            !== rowsPerPage

                        ) {

                            onRowsPerPageChange({

                                target: {

                                    value:
                                        model.pageSize,

                                },

                            });

                        }

                    }}

                    onRowClick={(params) => {

                        if (

                            hasPermission(

                                "payments.view",

                            )

                        ) {

                            onRowClick?.(

                                params.row,

                            );

                        }

                    }}

                    pageSizeOptions={[

                        10,

                        25,

                        50,

                    ]}

                    sx={{

                        border: 0,

                        "& .MuiDataGrid-columnHeaders": {

                            fontWeight: 700,

                            backgroundColor:
                                "background.paper",

                        },

                        "& .MuiDataGrid-cell": {

                            display: "flex",

                            alignItems: "center",

                        },

                        "& .MuiDataGrid-row": {

                            cursor:

                                hasPermission(

                                    "payments.view",

                                )

                                    ? "pointer"

                                    : "default",

                        },

                        "& .MuiDataGrid-row:nth-of-type(odd)": {

                            backgroundColor: "grey.50",

                        },

                        "& .MuiDataGrid-row:hover": {

                            cursor: "pointer",

                        },

                        "& .MuiDataGrid-cell:focus": {

                            outline: "none",

                        },

                        "& .MuiDataGrid-cell:focus-within": {

                            outline: "none",

                        },

                        "& .MuiDataGrid-columnHeader:focus": {

                            outline: "none",

                        },

                        "& .MuiDataGrid-columnHeader:focus-within": {

                            outline: "none",

                        },

                        "& .MuiDataGrid-footerContainer": {

                            borderTop: 1,

                            borderColor:
                                "divider",

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