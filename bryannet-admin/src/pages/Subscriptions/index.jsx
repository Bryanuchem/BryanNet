import {
    useMemo,
    useState,
} from "react";

import {
    Alert,
    Box,
    Button,
    CircularProgress,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";
import SyncIcon from "@mui/icons-material/Sync";

import PageHeader from "../../components/common/PageHeader";
import AppSnackbar from "../../components/common/AppSnackbar";
import FilterToolbar from "../../components/common/FilterToolbar";
import SearchBar from "../../components/common/SearchBar";
import ExportCsvButton from "../../components/common/ExportCsvButton";

import SubscriptionFilters from "../../components/subscriptions/SubscriptionFilters";
import SubscriptionTable from "../../components/subscriptions/SubscriptionTable";
import SubscriptionPurchaseDialog from "../../components/subscriptions/SubscriptionPurchaseDialog";
import SubscriptionDetailsDrawer from "../../components/subscriptions/SubscriptionDetailsDrawer";

import {
    useSubscriptions,
} from "../../hooks/useSubscriptions";

import {
    usePurchaseSubscription,
} from "../../hooks/usePurchaseSubscription";

import {
    useCancelSubscription,
} from "../../hooks/useCancelSubscription";

import {
    useProcessSubscriptions,
} from "../../hooks/useProcessSubscriptions";

import {
    useCustomers,
} from "../../hooks/useCustomers";

import {
    usePlans,
} from "../../hooks/usePlans";

import {

    useCurrentPermissions,

} from "../../hooks/useCurrentPermissions";

function Subscriptions() {

    const {

        hasPermission,

    } = useCurrentPermissions();

    const [
        page,
        setPage,
    ] = useState(0);

    const [
        rowsPerPage,
        setRowsPerPage,
    ] = useState(10);

    const [
        searchTerm,
        setSearchTerm,
    ] = useState("");

    const [
        customerFilter,
        setCustomerFilter,
    ] = useState("");

    const [
        planFilter,
        setPlanFilter,
    ] = useState("");

    const [
        statusFilter,
        setStatusFilter,
    ] = useState("");

    const {
        data,
        isLoading,
        error,
        refetch,
    } = useSubscriptions({

        page: page + 1,

        pageSize: rowsPerPage,

        search: searchTerm,

        customerId:
            customerFilter || undefined,

        planId:
            planFilter || undefined,

        status:
            statusFilter || undefined,

    });

    const subscriptions =
        data?.items ?? [];

    const total =
        data?.total ?? 0;

    const {
        data: customersData,
    } = useCustomers();

    const {
        data: plansData,
    } = usePlans();

    const purchaseSubscription =
        usePurchaseSubscription();

    const cancelSubscription =
        useCancelSubscription();

    const processSubscriptions =
        useProcessSubscriptions();

    const [
        purchaseDialogOpen,
        setPurchaseDialogOpen,
    ] = useState(false);

    const [
        drawerOpen,
        setDrawerOpen,
    ] = useState(false);

    const [
        selectedSubscription,
        setSelectedSubscription,
    ] = useState(null);

    const [
        snackbar,
        setSnackbar,
    ] = useState({

        open: false,

        severity: "success",

        message: "",

    });

    const customers = useMemo(() => {

        return (
            customersData?.items ??
            customersData ??
            []
        );

    }, [customersData]);

    const plans = useMemo(() => {

        return (
            plansData?.items ??
            plansData ??
            []
        );

    }, [plansData]);

    const sortedCustomers = useMemo(() => {

        return [...customers].sort(
            (a, b) =>
                (a.full_name ?? "").localeCompare(
                    b.full_name ?? "",
                ),
        );

    }, [customers]);

    const sortedPlans = useMemo(() => {

        return [...plans].sort(
            (a, b) =>
                (a.plan_name ?? "").localeCompare(
                    b.plan_name ?? "",
                ),
        );

    }, [plans]);

    const handleOpenPurchaseDialog =
        () => {

            if (

                !hasPermission(

                    "subscriptions.purchase",

                )

            ) {

                return;

            }

            setPurchaseDialogOpen(

                true,

            );

        };

    const handleClosePurchaseDialog =
        () => {

            setPurchaseDialogOpen(
                false,
            );

        };

    const handleOpenDrawer = (

        subscription,

    ) => {

        if (

            !hasPermission(

                "subscriptions.view",

            )

        ) {

            return;

        }

        setSelectedSubscription(

            subscription,

        );

        setDrawerOpen(

            true,

        );

    };

    const handleCloseDrawer =
        () => {

            setSelectedSubscription(
                null,
            );

            setDrawerOpen(false);

        };

    const handlePurchase =
        async (formData) => {

            try {

                await purchaseSubscription.mutateAsync(
                    formData,
                );

                setSnackbar({

                    open: true,

                    severity:
                        "success",

                    message:
                        "Subscription purchased successfully.",

                });

                handleClosePurchaseDialog();

            } catch (error) {

                setSnackbar({

                    open: true,

                    severity:
                        "error",

                    message:

                        error.response?.data
                            ?.detail ??

                        "Purchase failed.",

                });

            }

        };

    const handleCancel =
        async (

            subscriptionId,

        ) => {

            if (

                !hasPermission(

                    "subscriptions.cancel",

                )

            ) {

                return;

            }

            try {

                await cancelSubscription.mutateAsync(

                    subscriptionId,

                );

                setSnackbar({

                    open: true,

                    severity: "success",

                    message:

                        "Subscription cancelled successfully.",

                });

            } catch (error) {

                setSnackbar({

                    open: true,

                    severity: "error",

                    message:

                        error.response?.data?.detail ??

                        "Cancellation failed.",

                });

            }

        };

    const handleProcessSubscriptions =
        async () => {

            if (

                !hasPermission(

                    "subscriptions.process",

                )

            ) {

                return;

            }

            try {

                await processSubscriptions.mutateAsync();

                setSnackbar({

                    open: true,

                    severity: "success",

                    message:

                        "Subscription processing completed.",

                });

            } catch (error) {

                setSnackbar({

                    open: true,

                    severity: "error",

                    message:

                        error.response?.data?.detail ??

                        "Processing failed.",

                });

            }

        };

    const handleClearFilters =
        () => {

            setSearchTerm("");

            setCustomerFilter("");

            setPlanFilter("");

            setStatusFilter("");

            setPage(0);

        };

    const handleCloseSnackbar =
        () => {

            setSnackbar(
                (previous) => ({

                    ...previous,

                    open: false,

                }),
            );

        };

    const handleChangePage = (
        event,
        newPage,
    ) => {

        setPage(newPage);

    };

    const handleChangeRowsPerPage = (
        event,
    ) => {

        setRowsPerPage(
            parseInt(
                event.target.value,
                10,
            ),
        );

        setPage(0);

    };

    if (isLoading) {

        return (

            <Box
                display="flex"
                justifyContent="center"
                py={8}
            >

                <CircularProgress />

            </Box>

        );

    }

    if (error) {

        return (

            <Alert severity="error">

                Failed to load subscriptions.

            </Alert>

        );

    }

    return (

        <>

            <PageHeader
                title="Subscriptions"
                subtitle="Manage customer subscriptions."
            />

            <Box
                sx={{
                    display: "flex",
                    gap: 2,
                    mb: 3,
                    mt: 3,
                }}
            >

            {hasPermission(

                "subscriptions.purchase",

            ) && (

                <Button

                    variant="contained"

                    startIcon={<AddIcon />}

                    onClick={

                        handleOpenPurchaseDialog

                    }

                >

                    Purchase Subscription

                </Button>

            )}

            {hasPermission(

                "subscriptions.process",

            ) && (

                <Button

                    variant="outlined"

                    startIcon={<SyncIcon />}

                    onClick={

                        handleProcessSubscriptions

                    }

                >

                    Process Expired

                </Button>

            )}

            </Box>

            <FilterToolbar>

                <SearchBar
                    placeholder="Search by customer or plan..."
                    value={searchTerm}
                    onChange={(event) => {

                        setSearchTerm(
                            event.target.value,
                        );

                        setPage(0);

                    }}
                    sx={{
                        flex: 1,
                    }}
                />

                <SubscriptionFilters

                    customers={
                        sortedCustomers
                    }

                    plans={
                        sortedPlans
                    }

                    customerId={
                        customerFilter
                    }

                    planId={
                        planFilter
                    }

                    status={
                        statusFilter
                    }

                    onCustomerChange={(
                        event,
                    ) => {

                        setCustomerFilter(
                            event.target.value,
                        );

                        setPage(0);

                    }}

                    onPlanChange={(
                        event,
                    ) => {

                        setPlanFilter(
                            event.target.value,
                        );

                        setPage(0);

                    }}

                    onStatusChange={(
                        event,
                    ) => {

                        setStatusFilter(
                            event.target.value,
                        );

                        setPage(0);

                    }}

                    onRefresh={
                        refetch
                    }

                    onClear={
                        handleClearFilters
                    }

                />

                <ExportCsvButton

                    filename="subscriptions"

                    rows={
                        subscriptions
                    }

                    columns={[

                        {
                            key: "customer_name",
                            label: "Customer",
                        },

                        {
                            key: "plan_name",
                            label: "Plan",
                        },

                        {
                            key: "status",
                            label: "Status",
                        },

                        {
                            key: "created_at",
                            label: "Created",
                        },

                        {
                            key: "expiry_date",
                            label: "Expiry",
                        },

                        {
                            key: "remaining_days",
                            label: "Remaining Days",
                        },

                    ]}

                />

            </FilterToolbar>

            <SubscriptionTable
                subscriptions={
                    subscriptions
                }
                loading={isLoading}
                page={page}
                rowsPerPage={rowsPerPage}
                total={total}
                onPageChange={
                    handleChangePage
                }
                onRowsPerPageChange={
                    handleChangeRowsPerPage
                }
                onRowClick={
                    handleOpenDrawer
                }
                onCancel={
                    handleCancel
                }
            />

            {hasPermission(

                "subscriptions.purchase",

            ) && (

                <SubscriptionPurchaseDialog

                    open={

                        purchaseDialogOpen

                    }

                    customers={

                        sortedCustomers

                    }

                    plans={

                        sortedPlans

                    }

                    onClose={

                        handleClosePurchaseDialog

                    }

                    onSubmit={

                        handlePurchase

                    }

                />

            )}

            {hasPermission(

                "subscriptions.view",

            ) && (

                <SubscriptionDetailsDrawer

                    open={

                        drawerOpen

                    }

                    subscription={

                        selectedSubscription

                    }

                    onClose={

                        handleCloseDrawer

                    }

                />

            )}

            <AppSnackbar
                open={
                    snackbar.open
                }
                severity={
                    snackbar.severity
                }
                message={
                    snackbar.message
                }
                onClose={
                    handleCloseSnackbar
                }
            />

        </>

    );

}

export default Subscriptions;            