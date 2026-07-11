import { useState } from "react";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";

import PersonAddIcon from "@mui/icons-material/PersonAdd";

import SearchBar from "../../components/common/SearchBar";
import PageHeader from "../../components/common/PageHeader";
import AppSnackbar from "../../components/common/AppSnackbar";
import FilterToolbar from "../../components/common/FilterToolbar";
import ExportCsvButton from "../../components/common/ExportCsvButton";

import CustomerTable from "../../components/customers/CustomerTable";
import CustomerDialog from "../../components/customers/CustomerDialog";
import CustomerDetailsDrawer from "../../components/customers/CustomerDetailsDrawer";
import CustomerFilters from "../../components/customers/CustomerFilters";

import { useCustomers } from "../../hooks/useCustomers";
import { useCustomerSearch } from "../../hooks/useCustomerSearch";
import { useCreateCustomer } from "../../hooks/useCreateCustomer";
import { useUpdateCustomer } from "../../hooks/useUpdateCustomer";
import { useActivateCustomer} from "../../hooks/useActivateCustomer";
import { useDeactivateCustomer } from "../../hooks/useDeactivateCustomer";

import {

    useCurrentPermissions,

} from "../../hooks/useCurrentPermissions";

function Customers() {
    const {
        data: customers = [],
        isLoading,
        error,
        refetch,
    } = useCustomers();

    const createCustomer =
        useCreateCustomer();

    const updateCustomer =
        useUpdateCustomer();

    const activateCustomer =
        useActivateCustomer();

    const deactivateCustomer =
        useDeactivateCustomer();        

    const {
        searchTerm,
        setSearchTerm,
        filteredCustomers,
    } = useCustomerSearch(customers);

    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] =
        useState(10);

    const [
        registrationFilter,
        setRegistrationFilter,
    ] = useState("all");

    const [
        statusFilter,
        setStatusFilter,
    ] = useState("all");

    const {

        hasPermission,

    } = useCurrentPermissions();

    const [
        selectedCustomer,
        setSelectedCustomer,
    ] = useState(null);

    const [drawerOpen, setDrawerOpen] =
        useState(false);

    const [dialogOpen, setDialogOpen] =
        useState(false);

    const [snackbar, setSnackbar] =
        useState({
            open: false,
            message: "",
            severity: "success",
        });

    const handleChangePage = (
        event,
        newPage
    ) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (
        event
    ) => {
        setRowsPerPage(
            parseInt(event.target.value, 10)
        );
        setPage(0);
    };

    const handleCustomerClick = (

        customer,

    ) => {

        if (

            !hasPermission(

                "customers.view",

            )

        ) {

            return;

        }

        setSelectedCustomer(

            customer,

        );

        setDrawerOpen(

            true,

        );

    };

    const handleDrawerClose = () => {
        setDrawerOpen(false);
        setSelectedCustomer(null);
    };

    const handleOpenDialog = () => {

        if (

            !hasPermission(

                "customers.create",

            )

        ) {

            return;

        }

        setSelectedCustomer(

            null,

        );

        setDialogOpen(

            true,

        );

    };

    const handleEditCustomer = (

        customer,

    ) => {

        if (

            !hasPermission(

                "customers.edit",

            )

        ) {

            return;

        }

        setSelectedCustomer(

            customer,

        );

        setDialogOpen(

            true,

        );

    };

    const handleCloseDialog = () => {
        setDialogOpen(false);
        setSelectedCustomer(null);
    };

    const visibleCustomers =
        filteredCustomers.filter(
            (customer) => {

                if (
                    registrationFilter !== "all"
                ) {

                    const registered =
                        registrationFilter ===
                        "registered";

                    if (
                        customer.is_registered !==
                        registered
                    ) {

                        return false;

                    }

                }

                if (
                    statusFilter !== "all" &&
                    customer.status !==
                        statusFilter
                ) {

                    return false;

                }

                return true;

            },
        );

    const handleSubmitCustomer =
        async (formData) => {
            try {
                if (selectedCustomer) {
                    await updateCustomer.mutateAsync({
                        customerId:
                            selectedCustomer.customer_id,
                        customerData:
                            formData,
                    });

                    setSnackbar({
                        open: true,
                        message:
                            "Customer updated successfully.",
                        severity: "success",
                    });
                } else {
                    await createCustomer.mutateAsync(
                        formData
                    );

                    setSnackbar({
                        open: true,
                        message:
                            "Customer created successfully.",
                        severity: "success",
                    });
                }

                handleCloseDialog();
            } catch (err) {
                console.error(err);

                setSnackbar({
                    open: true,
                    message:
                        err.response?.data?.detail ||
                        "Operation failed.",
                    severity: "error",
                });
            }
        };

    const handleToggleStatus = async (

        customer,

    ) => {

        const canToggle =

            customer.status === "active"

                ? hasPermission(

                    "customers.deactivate",

                )

                : hasPermission(

                    "customers.activate",

                );

        if (

            !canToggle

        ) {

            return;

        }

        try {

            if (

                customer.status === "active"

            ) {

                await deactivateCustomer.mutateAsync(

                    customer.customer_id,

                );

                setSnackbar({

                    open: true,

                    message:

                        "Customer deactivated successfully.",

                    severity: "success",

                });

            } else {

                await activateCustomer.mutateAsync(

                    customer.customer_id,

                );

                setSnackbar({

                    open: true,

                    message:

                        "Customer activated successfully.",

                    severity: "success",

                });

            }

        } catch (err) {

            console.error(

                err,

            );

            setSnackbar({

                open: true,

                message:

                    err.response?.data?.detail ??

                    "Operation failed.",

                severity: "error",

            });

        }

    };

    const handleClearFilters = () => {

        setSearchTerm("");

        setRegistrationFilter(
            "all",
        );

        setStatusFilter(
            "all",
        );

        setPage(0);

    };

    const handleCloseSnackbar = () => {
        setSnackbar((prev) => ({
            ...prev,
            open: false,
        }));
    };

    if (error) {
        return (
            <>
                <PageHeader
                    title="Customers"
                    subtitle="Manage registered customers."
                />

                <p>
                    Failed to load
                    customers.
                </p>
            </>
        );
    }

    return (
        <>
            <PageHeader
                title="Customers"
                subtitle="Manage registered customers."
            />

                {hasPermission(

                    "customers.create",

                ) && (

                    <Box

                        sx={{

                            mt: 3,

                            mb: 2,

                        }}

                    >

                        <Button

                            variant="contained"

                            startIcon={<PersonAddIcon />}

                            onClick={

                                handleOpenDialog

                            }

                        >

                            New Customer

                        </Button>

                    </Box>

                )}

            <FilterToolbar>
                <SearchBar
                    value={searchTerm}
                    onChange={(event) => {
                        setSearchTerm(event.target.value);
                        setPage(0);
                    }}
                    placeholder="Search by name or phone number..."
                    sx={{
                        flex: 1,
                    }}
                />

                <CustomerFilters
                    registration={registrationFilter}
                    status={statusFilter}
                    onRegistrationChange={(event) => {
                        setRegistrationFilter(
                            event.target.value,
                        );
                        setPage(0);
                    }}
                    onStatusChange={(event) => {
                        setStatusFilter(
                            event.target.value,
                        );
                        setPage(0);
                    }}
                    onRefresh={refetch}
                    onClear={handleClearFilters}
                />

                <ExportCsvButton
                    filename="customers"
                    rows={filteredCustomers}
                    columns={[
                        {
                            key: "full_name",
                            label: "Customer",
                        },
                        {
                            key: "phone_number",
                            label: "Phone Number",
                        },
                        {
                            key: "status",
                            label: "Status",
                            formatter: (value) =>
                                value
                                    ? value.charAt(0).toUpperCase() +
                                    value.slice(1)
                                    : "",
                        },
                        {
                            key: "is_registered",
                            label: "Registered",
                            formatter: (value) =>
                                value ? "Yes" : "No",
                        },
                        {
                            key: "telegram_user_id",
                            label: "Telegram",
                            formatter: (value) =>
                                value
                                    ? "Linked"
                                    : "Not Linked",
                        },
                    ]}
                />
            </FilterToolbar>

            <CustomerTable
                customers={visibleCustomers}
                loading={isLoading}
                searchTerm={searchTerm}
                page={page}
                rowsPerPage={rowsPerPage}
                onPageChange={handleChangePage}
                onRowsPerPageChange={
                    handleChangeRowsPerPage
                }
                onRowClick={handleCustomerClick}
                onEdit={handleEditCustomer}
                onToggleStatus={
                    handleToggleStatus
                }
            />

            {(

                hasPermission(

                    "customers.create",

                ) ||

                hasPermission(

                    "customers.edit",

                )

            ) && (

                <CustomerDialog

                    open={

                        dialogOpen

                    }

                    onClose={

                        handleCloseDialog

                    }

                    onSubmit={

                        handleSubmitCustomer

                    }

                    customer={

                        selectedCustomer

                    }

                />

            )}

            {hasPermission(

                "customers.view",

            ) && (

                <CustomerDetailsDrawer

                    open={

                        drawerOpen

                    }

                    customer={

                        selectedCustomer

                    }

                    onClose={

                        handleDrawerClose

                    }

                />

            )}

            <AppSnackbar
                open={snackbar.open}
                onClose={handleCloseSnackbar}
                message={snackbar.message}
                severity={snackbar.severity}
            />
        </>
    );
}

export default Customers;    