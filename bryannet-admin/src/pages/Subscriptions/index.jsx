import { useMemo, useState } from "react";

import {
    Alert,
    Box,
    Snackbar,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";

import PageHeader from "../../components/common/PageHeader";
import TableToolbar from "../../components/common/TableToolbar";
import ConfirmDialog from "../../components/common/ConfirmDialog";

import SubscriptionTable from "../../components/subscriptions/SubscriptionTable";
import SubscriptionDialog from "../../components/subscriptions/SubscriptionDialog";
import SubscriptionPurchaseDialog from "../../components/subscriptions/SubscriptionPurchaseDialog";

import {
    useCustomers,
} from "../../hooks/useCustomers";

import {
    usePlans,
} from "../../hooks/usePlans";

import {
    useDeleteSubscription,
    useRenewSubscription,
    useSubscriptions,
    useUpdateSubscription,
    useUpdateSubscriptionStatus,
    usePurchaseSubscription,
} from "../../hooks/useSubscriptions";

function Subscriptions() {

    const {
        data: customers = [],
    } = useCustomers();

    const {
        data: plans = [],
    } = usePlans();

    const {
        data: subscriptions = [],
        isLoading,
        refetch,
    } = useSubscriptions();

    const purchaseSubscription =
        usePurchaseSubscription();

    const updateSubscription =
        useUpdateSubscription();

    const updateSubscriptionStatus =
        useUpdateSubscriptionStatus();

    const renewSubscription =
        useRenewSubscription();

    const deleteSubscription =
        useDeleteSubscription();

    const [search, setSearch] =
        useState("");

    const [
        statusFilter,
        setStatusFilter,
    ] = useState("all");

    const [
        dialogOpen,
        setDialogOpen,
    ] = useState(false);

    const [
        purchaseDialogOpen,
        setPurchaseDialogOpen,
    ] = useState(false);

    const [
        dialogMode,
        setDialogMode,
    ] = useState("view");

    const [
        selectedSubscription,
        setSelectedSubscription,
    ] = useState(null);

    const [
        confirmOpen,
        setConfirmOpen,
    ] = useState(false);

    const [
        confirmTitle,
        setConfirmTitle,
    ] = useState("");

    const [
        confirmMessage,
        setConfirmMessage,
    ] = useState("");

    const [
        confirmAction,
        setConfirmAction,
    ] = useState(null);

    const [
        snackbar,
        setSnackbar,
    ] = useState({
        open: false,
        severity: "success",
        message: "",
    });

    const [
        page,
        setPage,
    ] = useState(0);

    const [
        rowsPerPage,
        setRowsPerPage,
    ] = useState(10);

    const filteredSubscriptions =
        useMemo(() => {

            return subscriptions.filter(
                (subscription) => {

                    const searchTerm =
                        search.toLowerCase();

                    const matchesSearch =

                        subscription.customer_name
                            ?.toLowerCase()
                            .includes(searchTerm)

                        ||

                        subscription.plan_name
                            ?.toLowerCase()
                            .includes(searchTerm)

                        ||

                        String(
                            subscription.subscription_id
                        ).includes(searchTerm);

                    let matchesStatus = true;

                    switch (statusFilter) {

                        case "active":
                        case "queued":
                        case "expired":
                        case "suspended":
                        case "cancelled":

                            matchesStatus =
                                subscription.status ===
                                statusFilter;

                            break;

                        case "expiring":

                            matchesStatus =

                                subscription.status ===
                                "active"

                                &&

                                subscription.remaining_days <= 7;

                            break;

                        default:

                            matchesStatus = true;

                    }

                    return (
                        matchesSearch &&
                        matchesStatus
                    );

                }

            );

        }, [
            subscriptions,
            search,
            statusFilter,
        ]);

    const filters = [

        {
            value: "all",
            label: "All",
        },

        {
            value: "active",
            label: "Active",
        },

        {
            value: "queued",
            label: "Queued",
        },

        {
            value: "expired",
            label: "Expired",
        },

        {
            value: "suspended",
            label: "Suspended",
        },

        {
            value: "cancelled",
            label: "Cancelled",
        },

        {
            value: "expiring",
            label: "Expiring Soon",
        },

    ];

    const handleCreate = () => {

        setSelectedSubscription({

            customer_id: "",

            plan_id: "",

        });

        setPurchaseDialogOpen(true);

    };

    const handleView = (
        subscription
    ) => {

        setSelectedSubscription(
            subscription
        );

        setDialogMode("view");

        setDialogOpen(true);

    };

    const handleEdit = (
        subscription
    ) => {

        setSelectedSubscription({

            ...subscription,

        });

        setDialogMode("edit");

        setDialogOpen(true);

    };

    const handleDialogChange = (
        event
    ) => {

        const {
            name,
            value,
        } = event.target;

        setSelectedSubscription(
            (previous) => ({

                ...previous,

                [name]: value,

            })
        );

    };

    const handleDialogClose = () => {

        setDialogOpen(false);

        setSelectedSubscription(null);

    };

    const handlePurchaseDialogClose = () => {

        setPurchaseDialogOpen(false);

        setSelectedSubscription(null);

    };

    const handleSave = async () => {

        try {

            await updateSubscription.mutateAsync({

                subscriptionId:
                    selectedSubscription.subscription_id,

                data: {

                    plan_id:
                        selectedSubscription.plan_id,

                    start_date:
                        selectedSubscription.start_date,

                    expiry_date:
                        selectedSubscription.expiry_date,

                    activation_sequence:
                        selectedSubscription.activation_sequence,

                },

            });

            setSnackbar({

                open: true,

                severity: "success",

                message:
                    "Subscription updated successfully.",

            });

            handleDialogClose();

            refetch();

        } catch {

            setSnackbar({

                open: true,

                severity: "error",

                message:
                    "Failed to update subscription.",

            });

        }

    };

    const handlePurchase = async () => {

        try {

            await purchaseSubscription.mutateAsync({

                customer_id:
                    selectedSubscription.customer_id,

                plan_id:
                    selectedSubscription.plan_id,

            });

            setSnackbar({

                open: true,

                severity: "success",

                message:
                    "Subscription created successfully.",

            });

            handlePurchaseDialogClose();

            refetch();

        } catch {

            setSnackbar({

                open: true,

                severity: "error",

                message:
                    "Failed to create subscription.",

            });

        }

    };

    const handleStatusChange = (
        subscription,
        status
    ) => {

        setConfirmTitle(
            "Update Subscription"
        );

        setConfirmMessage(
            `Change subscription status to "${status}"?`
        );

        setConfirmAction(() => async () => {

            try {

                await updateSubscriptionStatus.mutateAsync({

                    subscriptionId:
                        subscription.subscription_id,

                    status,

                });

                setSnackbar({

                    open: true,

                    severity: "success",

                    message:
                        "Subscription status updated.",

                });

                refetch();

            } catch {

                setSnackbar({

                    open: true,

                    severity: "error",

                    message:
                        "Unable to update subscription.",

                });

            }

        });

        setConfirmOpen(true);

    };


    const handleRenew = (
        subscription
    ) => {

        setConfirmTitle(
            "Renew Subscription"
        );

        setConfirmMessage(
            `Queue another "${subscription.plan_name}" subscription for ${subscription.customer_name}?`
        );

        setConfirmAction(() => async () => {

            try {

                await renewSubscription.mutateAsync(
                    subscription.subscription_id
                );

                setSnackbar({

                    open: true,

                    severity: "success",

                    message:
                        "Subscription renewed successfully.",

                });

                refetch();

            } catch {

                setSnackbar({

                    open: true,

                    severity: "error",

                    message:
                        "Failed to renew subscription.",

                });

            }

        });

        setConfirmOpen(true);

    };


    const handleDelete = (
        subscription
    ) => {

        setConfirmTitle(
            "Delete Subscription"
        );

        setConfirmMessage(
            `Delete subscription #${subscription.subscription_id}?`
        );

        setConfirmAction(() => async () => {

            try {

                await deleteSubscription.mutateAsync(
                    subscription.subscription_id
                );

                setSnackbar({

                    open: true,

                    severity: "success",

                    message:
                        "Subscription deleted.",

                });

                refetch();

            } catch {

                setSnackbar({

                    open: true,

                    severity: "error",

                    message:
                        "Unable to delete subscription.",

                });

            }

        });

        setConfirmOpen(true);

    };

    const handleConfirm = async () => {

        if (confirmAction) {

            await confirmAction();

        }

        setConfirmOpen(false);

    };


    const handleClear = () => {

        setSearch("");

        setStatusFilter("all");

    };


    const handleSnackbarClose = () => {

        setSnackbar((previous) => ({

            ...previous,

            open: false,

        }));

    };


    return (

        <Box>

            <PageHeader
                title="Subscriptions"
                subtitle="Manage customer subscriptions, renew plans, suspend services and monitor subscription status."
                actionLabel="New Subscription"
                actionIcon={<AddIcon />}
                onAction={handleCreate}
            />

            <TableToolbar
                search={search}
                onSearchChange={setSearch}
                filter={statusFilter}
                onFilterChange={setStatusFilter}
                filters={filters}
                searchPlaceholder="Search by customer, plan or subscription ID..."
                onRefresh={refetch}
                onClear={handleClear}
            />

            <SubscriptionTable
                subscriptions={filteredSubscriptions}
                loading={isLoading}
                searchTerm={search}
                page={page}
                rowsPerPage={rowsPerPage}
                onPageChange={(event, newPage) =>
                    setPage(newPage)
                }
                onRowsPerPageChange={(event) => {

                    setRowsPerPage(
                        parseInt(
                            event.target.value,
                            10
                        )
                    );

                    setPage(0);

                }}
                onView={handleView}
                onEdit={handleEdit}
                onRenew={handleRenew}
                onStatusChange={handleStatusChange}
                onDelete={handleDelete}
            />

            <SubscriptionDialog
                open={dialogOpen}
                mode={dialogMode}
                subscription={selectedSubscription}
                onClose={handleDialogClose}
                onSave={handleSave}
                onChange={handleDialogChange}
            />

            <SubscriptionPurchaseDialog
                open={purchaseDialogOpen}
                customers={customers}
                plans={plans}
                subscription={selectedSubscription}
                onChange={handleDialogChange}
                onClose={handlePurchaseDialogClose}
                onPurchase={handlePurchase}
            />            

            <ConfirmDialog
                open={confirmOpen}
                title={confirmTitle}
                message={confirmMessage}
                onCancel={() =>
                    setConfirmOpen(false)
                }
                onConfirm={handleConfirm}
            />

            <Snackbar
                open={snackbar.open}
                autoHideDuration={4000}
                onClose={handleSnackbarClose}
                anchorOrigin={{
                    vertical: "bottom",
                    horizontal: "right",
                }}
            >
                <Alert
                    severity={snackbar.severity}
                    onClose={handleSnackbarClose}
                    variant="filled"
                    sx={{
                        width: "100%",
                    }}
                >
                    {snackbar.message}
                </Alert>
            </Snackbar>

        </Box>

    );

}

export default Subscriptions;