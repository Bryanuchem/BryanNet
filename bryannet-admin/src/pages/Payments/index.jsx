import {
    useState,
} from "react";

import Stack from "@mui/material/Stack";

import PaymentsRoundedIcon from "@mui/icons-material/PaymentsRounded";

import PageHeader from "../../components/common/PageHeader";
import StatCard from "../../components/common/StatCard";
import AppSnackbar from "../../components/common/AppSnackbar";
import ConfirmDialog from "../../components/common/ConfirmDialog";

import PaymentFilters from "../../components/payments/PaymentFilters";
import PaymentsTable from "../../components/payments/PaymentsTable";
import PaymentDialog from "../../components/payments/PaymentDialog";
import PaymentDetailsDialog from "../../components/payments/PaymentDetailsDialog";

import {
    usePayments,
    usePaymentStats,
    useCreatePayment,
    useUpdatePayment,
    useDeletePayment,
} from "../../hooks/usePayments";

function Payments() {

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

        data: payments = [],

        isLoading,

    } = usePayments({

        search,

        payment_channel:
            paymentChannel,

        status,

    });

    const {

        data: stats,

    } = usePaymentStats();

    const createPaymentMutation =
        useCreatePayment();

    const updatePaymentMutation =
        useUpdatePayment();

    const deletePaymentMutation =
        useDeletePayment();

    const [

        paymentDialogOpen,

        setPaymentDialogOpen,

    ] = useState(false);

    const [

        paymentDetailsOpen,

        setPaymentDetailsOpen,

    ] = useState(false);

    const [

        confirmDeleteOpen,

        setConfirmDeleteOpen,

    ] = useState(false);

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

    const handleCreate = () => {

        setSelectedPayment(null);

        setPaymentDialogOpen(true);

    };

    const handleView = (
        payment,
    ) => {

        setSelectedPayment(payment);

        setPaymentDetailsOpen(true);

    };

    const handleEdit = (
        payment,
    ) => {

        setSelectedPayment(payment);

        setPaymentDialogOpen(true);

    };

    const handleDelete = (
        payment,
    ) => {

        setSelectedPayment(payment);

        setConfirmDeleteOpen(true);

    };

    const handleClosePaymentDialog = () => {

        setPaymentDialogOpen(false);

        setSelectedPayment(null);

    };

    const handleClosePaymentDetails = () => {

        setPaymentDetailsOpen(false);

        setSelectedPayment(null);

    };

    const handleCloseDeleteDialog = () => {

        setConfirmDeleteOpen(false);

        setSelectedPayment(null);

    };

    const handleCloseSnackbar = () => {

        setSnackbar((previous) => ({

            ...previous,

            open: false,

        }));

    };

    const handleSubmit = async (
        paymentData,
    ) => {

        try {

            if (selectedPayment) {

                await updatePaymentMutation.mutateAsync({

                    paymentId:
                        selectedPayment.payment_id,

                    data:
                        paymentData,

                });

                setSnackbar({

                    open: true,

                    severity: "success",

                    message:
                        "Payment updated successfully.",

                });

            } else {

                await createPaymentMutation.mutateAsync(

                    paymentData,

                );

                setSnackbar({

                    open: true,

                    severity: "success",

                    message:
                        "Payment recorded successfully.",

                });

            }

            handleClosePaymentDialog();

        } catch {

            setSnackbar({

                open: true,

                severity: "error",

                message:
                    "Unable to save payment.",

            });

        }

    };

    const handleConfirmDelete = async () => {

        if (!selectedPayment) {

            return;

        }

        try {

            await deletePaymentMutation.mutateAsync(

                selectedPayment.payment_id,

            );

            setSnackbar({

                open: true,

                severity: "success",

                message:
                    "Payment deleted successfully.",

            });

        } catch {

            setSnackbar({

                open: true,

                severity: "error",

                message:
                    "Unable to delete payment.",

            });

        }

        handleCloseDeleteDialog();

    };

    return (

        <Stack
            spacing={3}
        >

            <PageHeader

                title="Payments"

                subtitle="Manage customer payments and payment history."

                icon={

                    <PaymentsRoundedIcon
                        color="primary"
                    />

                }

                actionLabel="Record Payment"

                onAction={handleCreate}

            />

            <Stack

                direction={{

                    xs: "column",

                    md: "row",

                }}

                spacing={2}

            >

                <StatCard

                    title="Total Payments"

                    value={
                        stats?.total_payments ?? 0
                    }

                />

                <StatCard

                    title="Revenue"

                    value={`₦${Number(
                        stats?.total_revenue ?? 0,
                    ).toLocaleString()}`}

                />

                <StatCard

                    title="Successful"

                    value={
                        stats?.successful_payments ?? 0
                    }

                />

                <StatCard

                    title="Pending"

                    value={
                        stats?.pending_payments ?? 0
                    }

                />

            </Stack>

            <PaymentFilters

                search={search}

                onSearchChange={setSearch}

                paymentChannel={
                    paymentChannel
                }

                onPaymentChannelChange={(event) =>

                    setPaymentChannel(
                        event.target.value,
                    )

                }

                status={status}

                onStatusChange={(event) =>

                    setStatus(
                        event.target.value,
                    )

                }

                onClear={() => {

                    setSearch("");

                    setPaymentChannel("");

                    setStatus("");

                }}

                onRefresh={() => {

                    window.location.reload();

                }}

            />

            <PaymentsTable

                payments={payments}

                loading={isLoading}

                onView={handleView}

                onEdit={handleEdit}

                onDelete={handleDelete}

            />

            <PaymentDialog

                open={paymentDialogOpen}

                loading={

                    createPaymentMutation.isPending ||

                    updatePaymentMutation.isPending

                }

                initialValues={
                    selectedPayment
                }

                onClose={
                    handleClosePaymentDialog
                }

                onSubmit={
                    handleSubmit
                }

            />

            <PaymentDetailsDialog

                open={paymentDetailsOpen}

                payment={
                    selectedPayment
                }

                onClose={
                    handleClosePaymentDetails
                }

            />

            <ConfirmDialog

                open={confirmDeleteOpen}

                title="Delete Payment"

                message={`Are you sure you want to delete payment "${selectedPayment?.payment_reference ?? ""}"? This action cannot be undone.`}

                confirmText="Delete"

                confirmColor="error"

                loading={

                    deletePaymentMutation.isPending

                }

                onClose={
                    handleCloseDeleteDialog
                }

                onConfirm={
                    handleConfirmDelete
                }

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