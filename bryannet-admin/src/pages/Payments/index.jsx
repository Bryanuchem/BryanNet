import {
    useState,
} from "react";

import Stack from "@mui/material/Stack";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button"

import PaymentsRoundedIcon from "@mui/icons-material/PaymentsRounded";

import PageHeader from "../../components/common/PageHeader";
import StatCard from "../../components/common/StatCard";
import AppSnackbar from "../../components/common/AppSnackbar";
import ConfirmDialog from "../../components/common/ConfirmDialog";

import PaymentFilters from "../../components/payments/PaymentFilters";
import PaymentsTable from "../../components/payments/PaymentsTable";
import PaymentDialog from "../../components/payments/PaymentDialog";
import PaymentDetailsDrawer from "../../components/payments/PaymentDetailsDrawer";

import {
    usePayments,
    usePaymentSummary,
} from "../../hooks/usePayments";

import {
    useCreatePayment,
} from "../../hooks/useCreatePayment";

import {
    useCompletePayment,
} from "../../hooks/useCompletePayment";

import {
    useCancelPayment,
} from "../../hooks/useCancelPayment";

import {
    useRefundPayment,
} from "../../hooks/useRefundPayment";

import {
    useExpirePayment,
} from "../../hooks/useExpirePayment";

import {
    usePaymentReceipt,
} from "../../hooks/usePaymentReceipt";

import {

    useCurrentPermissions,

} from "../../hooks/useCurrentPermissions";

function Payments() {

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
        search,
        setSearch,
    ] = useState("");

    const [
        paymentChannel,
        setPaymentChannel,
    ] = useState("");

    const [
        status,
        setStatus,
    ] = useState("");

    const {

        data,

        isLoading,

        refetch,

    } = usePayments({

        page: page + 1,

        pageSize: rowsPerPage,

        search,

        payment_channel:
            paymentChannel || undefined,

        status:
            status || undefined,

    });

    const payments =
        data?.items ?? [];

    const total =
        data?.total ?? 0;

    const {

        data: stats,

    } = usePaymentSummary();

    const createPayment =
        useCreatePayment();

    const completePayment =
        useCompletePayment();

    const cancelPayment =
        useCancelPayment();

    const refundPayment =
        useRefundPayment();

    const expirePayment =
        useExpirePayment();

    const printReceipt =
        usePaymentReceipt();

    const [

        paymentDialogOpen,

        setPaymentDialogOpen,

    ] = useState(false);

    const [

        drawerOpen,

        setDrawerOpen,

    ] = useState(false);

    const [

        confirmDialog,

        setConfirmDialog,

    ] = useState({

        open: false,

        title: "",

        message: "",

        action: null,

    });

    const [

        selectedPayment,

        setSelectedPayment,

    ] = useState(null);

    const [

        snackbar,

        setSnackbar,

    ] = useState({

        open: false,

        severity: "success",

        message: "",

    });

    const handleChangePage = (
        event,
        newPage,
    ) => {

        setPage(
            newPage,
        );

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

    const handleCreate = () => {

        if (

            !hasPermission(

                "payments.create",

            )

        ) {

            return;

        }

        setSelectedPayment(

            null,

        );

        setPaymentDialogOpen(

            true,

        );

    };

    const handleCloseDialog = () => {

        setPaymentDialogOpen(false);

        setSelectedPayment(null);

    };


    const handleOpenDrawer = (
        payment,
    ) => {

        setSelectedPayment(
            payment,
        );

        setDrawerOpen(
            true,
        );

    };

    const handleCloseDrawer = () => {

        setDrawerOpen(false);

        setSelectedPayment(null);

    };

    const handleSubmit = async (
        paymentData,
    ) => {

        try {

            await createPayment.mutateAsync(
                paymentData,
            );

            setSnackbar({

                open: true,

                severity: "success",

                message:
                    "Payment recorded successfully.",

            });

            handleCloseDialog();

        } catch (error) {

            setSnackbar({

                open: true,

                severity: "error",

                message:

                    error.response?.data?.detail ??

                    "Unable to record payment.",

            });

        }

    };

    const openConfirmation = (
        title,
        message,
        action,
    ) => {

        setConfirmDialog({

            open: true,

            title,

            message,

            action,

        });

    };

    const handleCloseConfirmation = () => {

        setConfirmDialog({

            open: false,

            title: "",

            message: "",

            action: null,

        });

    };

    const handleCloseSnackbar = () => {

        setSnackbar(

            (previous) => ({

                ...previous,

                open: false,

            }),

        );

    };

    const handleClearFilters = () => {

        setSearch("");

        setPaymentChannel("");

        setStatus("");

        setPage(0);

    };

    return (

        <Stack
            spacing={3}
        >

            <PageHeader
                title="Payments"
                subtitle="Manage customer payments and payment history."
            />

            {hasPermission(

                "payments.create",

            ) && (

                <Box

                    sx={{

                        mb: 3,

                    }}

                >

                    <Button

                        variant="contained"

                        startIcon={

                            <PaymentsRoundedIcon />

                        }

                        onClick={

                            handleCreate

                        }

                    >

                        Record Payment

                    </Button>

                </Box>

            )}      

            <Stack

                direction={{

                    xs: "column",

                    md: "row",

                }}

                spacing={2}

            >

            <Box sx={{ flex: 1 }}>
                <StatCard
                    title="Total Payments"
                    value={stats?.total_payments ?? 0}
                />
            </Box>

            <Box sx={{ flex: 1 }}>
                <StatCard
                    title="Revenue"
                    value={`₦${Number(
                        stats?.total_revenue ?? 0,
                    ).toLocaleString()}`}
                />
            </Box>

            <Box sx={{ flex: 1 }}>
                <StatCard
                    title="Successful"
                    value={stats?.successful_payments ?? 0}
                />
            </Box>

            <Box sx={{ flex: 1 }}>
                <StatCard
                    title="Pending"
                    value={stats?.pending_payments ?? 0}
                />
            </Box>
        </Stack>

            <PaymentFilters

                search={search}

                onSearchChange={(
                    event,
                ) => {

                    setSearch(
                        event.target.value,
                    );

                    setPage(0);

                }}

                paymentChannel={
                    paymentChannel
                }

                onPaymentChannelChange={(
                    event,
                ) => {

                    setPaymentChannel(
                        event.target.value,
                    );

                    setPage(0);

                }}

                status={
                    status
                }

                onStatusChange={(
                    event,
                ) => {

                    setStatus(
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

            <PaymentsTable

                payments={
                    payments
                }

                loading={
                    isLoading
                }

                page={
                    page
                }

                rowsPerPage={
                    rowsPerPage
                }

                total={
                    total
                }

                onPageChange={
                    handleChangePage
                }

                onRowsPerPageChange={
                    handleChangeRowsPerPage
                }

                onView={
                    handleOpenDrawer
                }

                onRowClick={
                    handleOpenDrawer
                }

                onPrintReceipt={(
                    payment,
                ) =>

                    printReceipt.mutate(
                        payment.payment_reference,
                    )

                }

                onComplete={(
                    payment,
                ) =>

                    openConfirmation(

                        "Complete Payment",

                        `Complete payment "${payment.payment_reference}"?`,

                async () => {

                    await completePayment.mutateAsync({

                        paymentReference:
                            payment.payment_reference,

                    });

                    await refetch({
                        throwOnError: true,
                    });

                    setSelectedPayment(null);

                    setDrawerOpen(false);

                    setSnackbar({

                        open: true,

                        severity: "success",

                        message:
                            "Payment completed successfully.",

                    });

                },
                    )

                }

                onCancel={(
                    payment,
                ) =>

                    openConfirmation(

                        "Cancel Payment",

                        `Cancel payment "${payment.payment_reference}"?`,

                        async () => {

                            await cancelPayment.mutateAsync(
                                payment.payment_reference,
                            );

                            await refetch({
                                throwOnError: true,
                            });

                            setSelectedPayment(null);

                            setDrawerOpen(false);

                            setSnackbar({

                                open: true,

                                severity: "success",

                                message:
                                    "Payment cancelled successfully.",

                            });

                        },

                    )

                }

                onRefund={(
                    payment,
                ) =>

                    openConfirmation(

                        "Refund Payment",

                        `Refund payment "${payment.payment_reference}"?`,

                        async () => {

                            await refundPayment.mutateAsync(
                                payment.payment_reference,
                            );

                            await refetch({
                                throwOnError: true,
                            });
                            setSelectedPayment(null);

                            setDrawerOpen(false);

                            setSnackbar({

                                open: true,

                                severity: "success",

                                message:
                                    "Payment refunded successfully.",

                            });

                        },

                    )

                }

                onExpire={(
                    payment,
                ) =>

                    openConfirmation(

                        "Expire Payment",

                        `Expire payment "${payment.payment_reference}"?`,

                        async () => {

                            await expirePayment.mutateAsync(
                                payment.payment_reference,
                            );

                            await refetch({
                                throwOnError: true,
                            });

                            setSelectedPayment(null);

                            setDrawerOpen(false);

                            setSnackbar({

                                open: true,

                                severity: "success",

                                message:
                                    "Payment expired successfully.",

                            });

                        },

                    )

                }

            />

            {hasPermission(

                "payments.create",

            ) && (

                <PaymentDialog

                    open={

                        paymentDialogOpen

                    }

                    loading={

                        createPayment.isPending

                    }

                    onClose={

                        handleCloseDialog

                    }

                    onSubmit={

                        handleSubmit

                    }

                />

            )}
            
            {hasPermission(

                "payments.view",

            ) && (

                <PaymentDetailsDrawer

                    open={

                        drawerOpen

                    }

                    payment={

                        selectedPayment

                    }

                    onClose={

                        handleCloseDrawer

                    }

                />

            )}


            <ConfirmDialog

                open={
                    confirmDialog.open
                }

                title={
                    confirmDialog.title
                }

                message={
                    confirmDialog.message
                }

                confirmText="Confirm"

                loading={

                    completePayment.isPending ||

                    cancelPayment.isPending ||

                    refundPayment.isPending ||

                    expirePayment.isPending

                }

                onClose={
                    handleCloseConfirmation
                }

                onConfirm={async () => {

                    if (
                        !confirmDialog.action
                    ) {

                        return;

                    }

                    try {

                        await confirmDialog.action();

                    } catch (error) {

                        setSnackbar({

                            open: true,

                            severity: "error",

                            message:

                                error.response?.data?.detail ??

                                "Operation failed.",

                        });

                    }

                    handleCloseConfirmation();

                }}

            />

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

        </Stack>

    );

}

export default Payments;                