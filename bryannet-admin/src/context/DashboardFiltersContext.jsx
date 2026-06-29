import {
    createContext,
    useContext,
    useMemo,
    useState,
} from "react";

const DashboardFiltersContext = createContext(null);

export function DashboardFiltersProvider({ children }) {

    const [filters, setFilters] = useState({
        year: new Date().getFullYear(),
        period: "month",
        startDate: null,
        endDate: null,
    });

    const updateFilters = (updates) => {

        setFilters((previous) => ({
            ...previous,
            ...updates,
        }));

    };

    const resetFilters = () => {

        setFilters({
            year: new Date().getFullYear(),
            period: "month",
            startDate: null,
            endDate: null,
        });

    };

    const value = useMemo(() => ({
        filters,
        updateFilters,
        resetFilters,
    }), [filters]);

    return (
        <DashboardFiltersContext.Provider value={value}>
            {children}
        </DashboardFiltersContext.Provider>
    );

}

function useDashboardFilters() {

    const context = useContext(DashboardFiltersContext);

    if (!context) {

        throw new Error(
            "useDashboardFilters must be used inside DashboardFiltersProvider."
        );

    }

    return context;

}

export {
    useDashboardFilters,
};

export default DashboardFiltersContext;