import { useState } from "react";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";

import PersonAddIcon from "@mui/icons-material/PersonAdd";

import SearchBar from "../../components/common/SearchBar";
import PageHeader from "../../components/common/PageHeader";
import AppSnackbar from "../../components/common/AppSnackbar";

import CustomerTable from "../../components/customers/CustomerTable";
import CustomerDialog from "../../components/customers/CustomerDialog";
import CustomerDetailsDrawer from "../../components/customers/CustomerDetailsDrawer";

import { useCustomers } from "../../hooks/useCustomers";
import { useCustomerSearch } from "../../hooks/useCustomerSearch";
import { useCreateCustomer } from "../../hooks/useCreateCustomer";
import { useUpdateCustomer } from "../../hooks/useUpdateCustomer";

function Customers() {
    const {
        data: customers = [],
        isLoading,
        error,
    } = useCustomers();

    const createCustomer =
        useCreateCustomer();

    const updateCustomer =
        useUpdateCustomer();

    const {
        searchTerm,
        setSearchTerm,
        filteredCustomers,
    } = useCustomerSearch(customers);

    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] =
        useState(10);

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
        customer
    ) => {
        setSelectedCustomer(customer);
        setDrawerOpen(true);
    };

    const handleDrawerClose = () => {
        setDrawerOpen(false);
        setSelectedCustomer(null);
    };

    const handleOpenDialog = () => {
        setSelectedCustomer(null);
        setDialogOpen(true);
    };

    const handleEditCustomer = (
        customer
    ) => {
        setSelectedCustomer(customer);
        setDialogOpen(true);
    };

    const handleCloseDialog = () => {
        setDialogOpen(false);
        setSelectedCustomer(null);
    };

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

            <Box sx={{ mt: 3, mb: 3 }}>
                <Button
                    variant="contained"
                    startIcon={<PersonAddIcon />}
                    onClick={handleOpenDialog}
                >
                    New Customer
                </Button>
            </Box>

            <SearchBar
                value={searchTerm}
                onChange={(event) => {
                    setSearchTerm(event.target.value);
                    setPage(0);
                }}
                placeholder="Search by name or phone..."
            />

            <CustomerTable
                customers={filteredCustomers}
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
            />

            <CustomerDialog
                open={dialogOpen}
                onClose={handleCloseDialog}
                onSubmit={handleSubmitCustomer}
                customer={selectedCustomer}
            />

            <CustomerDetailsDrawer
                open={drawerOpen}
                customer={selectedCustomer}
                onClose={handleDrawerClose}
            />

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