import { useState } from "react";
import { useCustomers } from "../../hooks/useCustomers";

import SearchBar from "../../components/common/SearchBar";
import PageHeader from "../../components/common/PageHeader";
import CustomerTable from "../../components/customers/CustomerTable";
import { useCustomerSearch } from "../../hooks/useCustomerSearch";
import CustomerDetailsDrawer from "../../components/customers/CustomerDetailsDrawer";

function Customers() {
    const {
        data: customers = [],
        isLoading,
        error,
    } = useCustomers();

    const {
        searchTerm,
        setSearchTerm,
        filteredCustomers,
    } = useCustomerSearch(customers);

    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(10);

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    const [selectedCustomer, setSelectedCustomer] = useState(null);
    const [drawerOpen, setDrawerOpen] = useState(false);


    const handleCustomerClick = (customer) => {
    setSelectedCustomer(customer);
    setDrawerOpen(true);
};

    const handleDrawerClose = () => {
        setDrawerOpen(false);
        setSelectedCustomer(null);
};

    if (error) {
        return (
            <>
                <PageHeader
                    title="Customers"
                    subtitle="Manage registered customers."
                />

                <p>Failed to load customers.</p>
            </>
        );
    }

    return (
        <>
            <PageHeader
                title="Customers"
                subtitle="Manage registered customers."
            />

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
                totalCustomers={customers.length}
                page={page}
                rowsPerPage={rowsPerPage}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
                onRowClick={handleCustomerClick}
            />
            
            <CustomerDetailsDrawer
                open={drawerOpen}
                customer={selectedCustomer}
                onClose={handleDrawerClose}
            />
           
        </>

    );
}

export default Customers;