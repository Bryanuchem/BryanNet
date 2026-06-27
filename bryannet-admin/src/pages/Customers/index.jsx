import { useCustomers } from "../../hooks/useCustomers";

import SearchBar from "../../components/common/SearchBar";
import PageHeader from "../../components/common/PageHeader";
import CustomerTable from "../../components/customers/CustomerTable";
import { useCustomerSearch } from "../../hooks/useCustomerSearch";

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
                onChange={(event) => setSearchTerm(event.target.value)}
                placeholder="Search by name or phone..."
            />

            <CustomerTable
                customers={filteredCustomers}
                loading={isLoading}
                searchTerm={searchTerm}
                totalCustomers={customers.length}
            />
           
        </>
    );
}

export default Customers;