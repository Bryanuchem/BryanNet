import {
    createContext,
    useContext,
    useState,
} from "react";

const LayoutContext = createContext(null);

export function LayoutProvider({ children }) {

    const [sidebarCollapsed, setSidebarCollapsed] =
        useState(false);

    const toggleSidebar = () => {

        setSidebarCollapsed(
            (prev) => !prev
        );

    };

    const value = {
        sidebarCollapsed,
        toggleSidebar,
    };

    return (
        <LayoutContext.Provider value={value}>
            {children}
        </LayoutContext.Provider>
    );
}

export function useLayout() {

    const context = useContext(LayoutContext);

    if (!context) {
        throw new Error(
            "useLayout must be used inside LayoutProvider."
        );
    }

    return context;

}