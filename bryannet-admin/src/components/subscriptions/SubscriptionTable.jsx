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

import VisibilityIcon from "@mui/icons-material/Visibility";
import EditIcon from "@mui/icons-material/Edit";
import AutorenewIcon from "@mui/icons-material/Autorenew";
import PauseCircleIcon from "@mui/icons-material/PauseCircle";
import PlayCircleIcon from "@mui/icons-material/PlayCircle";
import CancelIcon from "@mui/icons-material/Cancel";
import DeleteIcon from "@mui/icons-material/Delete";

import ActionMenu from "../common/ActionMenu";
import BadgeChip from "../common/BadgeChip";
import EmptyState from "../common/EmptyState";

function SubscriptionTable({
    subscriptions,
    loading,
    searchTerm,
    page,
    rowsPerPage,
    onPageChange,
    onRowsPerPageChange,
    onView,
    onEdit,
    onRenew,
    onStatusChange,
    onDelete,
}) {

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

    if (subscriptions.length === 0) {

        if (searchTerm) {
            return (
                <EmptyState
                    title="No matching subscriptions"
                    description="Try a different customer name, plan or status."
                />
            );
        }

        return (
            <EmptyState
                title="No subscriptions found"
                description="Customer subscriptions will appear here."
            />
        );
    }

    return (
        <Paper>

            <TableContainer
                sx={{
                    maxHeight: 650,
                }}
            >

                <Table stickyHeader>

                    <TableHead>

                        <TableRow>

                            <TableCell sx={{ fontWeight: 700 }}>
                                Customer
                            </TableCell>

                            <TableCell sx={{ fontWeight: 700 }}>
                                Plan
                            </TableCell>

                            <TableCell sx={{ fontWeight: 700 }}>
                                Status
                            </TableCell>

                            <TableCell sx={{ fontWeight: 700 }}>
                                Price
                            </TableCell>

                            <TableCell sx={{ fontWeight: 700 }}>
                                Remaining
                            </TableCell>

                            <TableCell sx={{ fontWeight: 700 }}>
                                Expiry Date
                            </TableCell>

                            <TableCell
                                align="center"
                                sx={{ fontWeight: 700 }}
                            >
                                Actions
                            </TableCell>

                        </TableRow>

                    </TableHead>

                    <TableBody>

                        {subscriptions
                            .slice(
                                page * rowsPerPage,
                                page * rowsPerPage + rowsPerPage
                            )
                            .map((subscription) => (

                                <TableRow
                                    key={
                                        subscription.subscription_id
                                    }
                                    hover
                                    sx={{
                                        "&:nth-of-type(odd)": {
                                            bgcolor: "#FAFAFA",
                                        },

                                        "&:hover": {
                                            bgcolor: "#F1F5F9",
                                        },
                                    }}
                                >

                                    <TableCell>
                                        {subscription.customer_name}
                                    </TableCell>

                                    <TableCell>
                                        {subscription.plan_name}
                                    </TableCell>

                                    <TableCell>

                                        <BadgeChip
                                            variant="status"
                                            value={
                                                subscription.status
                                            }
                                        />

                                    </TableCell>

                                    <TableCell>
                                        ₦
                                        {Number(
                                            subscription.price
                                        ).toLocaleString()}
                                    </TableCell>

                                    <TableCell>
                                        {
                                            subscription.remaining_days
                                        }{" "}
                                        days
                                    </TableCell>

                                    <TableCell>
                                        {new Date(
                                            subscription.expiry_date
                                        ).toLocaleDateString()}
                                    </TableCell>

                                    <TableCell
                                        align="center"
                                        onClick={(event) =>
                                            event.stopPropagation()
                                        }
                                    >

                                        <ActionMenu
                                            items={[
                                                {
                                                    label: "View Details",
                                                    icon: (
                                                        <VisibilityIcon fontSize="small" />
                                                    ),
                                                    onClick: () =>
                                                        onView(
                                                            subscription
                                                        ),
                                                },

                                                {
                                                    label: "Edit Subscription",
                                                    icon: (
                                                        <EditIcon fontSize="small" />
                                                    ),
                                                    onClick: () =>
                                                        onEdit(
                                                            subscription
                                                        ),
                                                },

                                                {
                                                    label: "Renew Subscription",
                                                    icon: (
                                                        <AutorenewIcon fontSize="small" />
                                                    ),
                                                    onClick: () =>
                                                        onRenew(
                                                            subscription
                                                        ),
                                                },

                                                subscription.status ===
                                                "active"
                                                    ? {
                                                          label:
                                                              "Suspend Subscription",
                                                          icon: (
                                                              <PauseCircleIcon fontSize="small" />
                                                          ),
                                                          onClick: () =>
                                                              onStatusChange(
                                                                  subscription,
                                                                  "suspended"
                                                              ),
                                                      }
                                                    : {
                                                          label:
                                                              "Reactivate Subscription",
                                                          icon: (
                                                              <PlayCircleIcon fontSize="small" />
                                                          ),
                                                          onClick: () =>
                                                              onStatusChange(
                                                                  subscription,
                                                                  "active"
                                                              ),
                                                      },

                                                {
                                                    label: "Cancel Subscription",
                                                    icon: (
                                                        <CancelIcon fontSize="small" />
                                                    ),
                                                    onClick: () =>
                                                        onStatusChange(
                                                            subscription,
                                                            "cancelled"
                                                        ),
                                                },

                                                {
                                                    label: "Delete Subscription",
                                                    icon: (
                                                        <DeleteIcon fontSize="small" />
                                                    ),
                                                    onClick: () =>
                                                        onDelete(
                                                            subscription
                                                        ),
                                                },
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
                count={subscriptions.length}
                page={page}
                rowsPerPage={rowsPerPage}
                onPageChange={onPageChange}
                onRowsPerPageChange={
                    onRowsPerPageChange
                }
                rowsPerPageOptions={[
                    5,
                    10,
                    25,
                    50,
                ]}
            />

        </Paper>
    );
}

export default SubscriptionTable;