import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    CircularProgress,
    Box,
} from "@mui/material";

import TablePagination from "@mui/material/TablePagination";
import ActionMenu from "../common/ActionMenu";
import VisibilityIcon from "@mui/icons-material/Visibility";
import EditIcon from "@mui/icons-material/Edit";
import BlockIcon from "@mui/icons-material/Block";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import EmptyState from "../common/EmptyState";

import BadgeChip from "../common/BadgeChip";

import {

    formatPhoneNumber,

} from "../../utils/customerFormatter";

import {

    useCurrentPermissions,

} from "../../hooks/useCurrentPermissions";

function CustomerTable({
    customers,
    loading,
    searchTerm,
    page,
    rowsPerPage,
    onPageChange,
    onRowsPerPageChange,
    onRowClick,
    onEdit,
    onToggleStatus,
})



{
    const {

        hasPermission,

    } = useCurrentPermissions();

    if (loading) {
        return (
            <Box
                sx={{
                    display: "flex",
                    justifyContent: "center",
                    py: 6,
                }}
            >
                <CircularProgress />
            </Box>
        );
    }

    if (customers.length === 0) {

        if (searchTerm) {
            return (
                <EmptyState
                    title="No matching customers"
                    description="Try searching with a different name or phone number."
                />
            );
        }

        return (

            <EmptyState

                title="No customers yet"

                description="Customers who register through Telegram will appear here."

            />

        );

    }

    return (
        <Paper>
            <TableContainer
                sx={{
                    maxHeight: 600,
                }}
>               <Table stickyHeader>
                    <TableHead>
                        <TableRow
                            sx={{
                                "&:nth-of-type(odd)": {
                                    bgcolor: "#FAFAFA",
                                },
                                "&:hover": {
                                    bgcolor: "#F1F5F9",
                                    cursor: "pointer",
                                },
                            }}
                        >
                            <TableCell
                                sx={{
                                    fontWeight: 700,
                                }}
                            >
                                Name

                            </TableCell>

                            <TableCell
                                sx={{
                                    fontWeight: 700,
                                }}
                            >
                                Phone

                            </TableCell>

                            <TableCell
                                sx={{
                                    fontWeight: 700,
                                }}
                            >
                                Registered
                            </TableCell>

                            <TableCell
                                sx={{
                                    fontWeight: 700,
                                }}
                            >
                                Status
                            </TableCell>

                            <TableCell
                                sx={{
                                    fontWeight: 700,
                                }}
                            >
                                Telegram
                            </TableCell>

                            <TableCell
                                align="center"
                                sx={{
                                    fontWeight: 700,
                                }}
                            >
                                Actions
                            </TableCell>

                            </TableRow>
                    </TableHead>

                    <TableBody>
                        {customers
                            .slice(
                                page * rowsPerPage,
                                page * rowsPerPage + rowsPerPage
                            )
                            .map((customer) => (

                        <TableRow

                            key={

                                customer.customer_id

                            }

                            hover

                            onClick={() => {

                                if (

                                    hasPermission(

                                        "customers.view",

                                    )

                                ) {

                                    onRowClick?.(

                                        customer,

                                    );

                                }

                            }}

                            sx={{

                                height: 60,

                                "&:nth-of-type(odd)": {

                                    bgcolor: "#FAFAFA",

                                },

                                "&:hover": {

                                    bgcolor: "#F1F5F9",

                                    cursor:

                                        hasPermission(

                                            "customers.view",

                                        )

                                            ? "pointer"

                                            : "default",

                                },

                            }}

                        >                                
                                <TableCell>
                                        {customer.full_name}
                                    </TableCell>

                                    <TableCell>
                                        {formatPhoneNumber(customer.phone_number)}
                                    </TableCell>

                                    <TableCell align="center">
                                        <BadgeChip
                                            label={
                                                customer.is_registered
                                                    ? "Registered"
                                                    : "Pending"
                                            }
                                            color={
                                                customer.is_registered
                                                    ? "success"
                                                    : "warning"
                                            }
                                        />
                                    </TableCell>

                                    <TableCell align="center">
                                        <BadgeChip
                                            label={
                                                customer.status === "active"
                                                    ? "Active"
                                                    : "Inactive"
                                            }
                                            color={
                                                customer.status === "active"
                                                    ? "success"
                                                    : "error"
                                            }
                                        />
                                    </TableCell>

                                    <TableCell align="center">
                                        <BadgeChip
                                            label={
                                                customer.telegram_user_id
                                                    ? "Linked"
                                                    : "Not Linked"
                                            }
                                            color={
                                                customer.telegram_user_id
                                                    ? "info"
                                                    : "default"
                                            }
                                        />
                                    </TableCell>

                                    <TableCell
                                        align="center"
                                        onClick={(event) => event.stopPropagation()}
                                    >
                                        <ActionMenu

                                            items={[

                                                ...(hasPermission(

                                                    "customers.view",

                                                )

                                                    ? [

                                                        {

                                                            label: "View Details",

                                                            icon: (

                                                                <VisibilityIcon

                                                                    fontSize="small"

                                                                />

                                                            ),

                                                            onClick: () =>

                                                                onRowClick?.(

                                                                    customer,

                                                                ),

                                                        },

                                                    ]

                                                    : []),

                                                ...(hasPermission(

                                                    "customers.edit",

                                                )

                                                    ? [

                                                        {

                                                            label: "Edit Customer",

                                                            icon: (

                                                                <EditIcon

                                                                    fontSize="small"

                                                                />

                                                            ),

                                                            onClick: () =>

                                                                onEdit?.(

                                                                    customer,

                                                                ),

                                                        },

                                                    ]

                                                    : []),

                                                ...(

                                                    customer.status === "active"

                                                        ? hasPermission(

                                                            "customers.deactivate",

                                                        )

                                                        : hasPermission(

                                                            "customers.activate",

                                                        )

                                                )

                                                    ? [

                                                        {

                                                            label:

                                                                customer.status === "active"

                                                                    ? "Deactivate Customer"

                                                                    : "Activate Customer",

                                                            icon:

                                                                customer.status === "active"

                                                                    ? (

                                                                        <BlockIcon

                                                                            fontSize="small"

                                                                        />

                                                                    )

                                                                    : (

                                                                        <CheckCircleIcon

                                                                            fontSize="small"

                                                                        />

                                                                    ),

                                                            onClick: () =>

                                                                onToggleStatus?.(

                                                                    customer,

                                                                ),

                                                        },

                                                    ]

                                                    : [],

                                            ]}

                                        />                            
                                    </TableCell>
                                </TableRow>
                            ))}
                    </TableBody>
                </Table>
            </TableContainer>

            <TablePagination
                component="div"
                count={customers.length}
                page={page}
                rowsPerPage={rowsPerPage}
                onPageChange={onPageChange}
                onRowsPerPageChange={onRowsPerPageChange}
                rowsPerPageOptions={[5, 10, 25]}
            />
        </Paper>
    );
}

export default CustomerTable;