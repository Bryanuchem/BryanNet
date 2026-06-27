import { useMemo, useState } from "react";

export function useCustomerSearch(customers) {
    const [searchTerm, setSearchTerm] = useState("");

    const filteredCustomers = useMemo(() => {
        const search = searchTerm.trim().toLowerCase();

        if (!search) {
            return customers;
        }

        return customers.filter((customer) => {
            const fullName = (customer.full_name || "").toLowerCase();

            const phone = (customer.phone_number || "")
                .replace(/\D/g, "");

            const searchDigits = search.replace(/\D/g, "");

            const matchesName =
                fullName.includes(search);

            const matchesPhone =
                searchDigits.length > 0 &&
                phone.includes(searchDigits);

            return matchesName || matchesPhone;
        });

    }, [customers, searchTerm]);

    return {
        searchTerm,
        setSearchTerm,
        filteredCustomers,
    };
}