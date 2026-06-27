import { Routes, Route } from "react-router-dom";

import Dashboard from "../pages/Dashboard";
import Customers from "../pages/Customers";
import Plans from "../pages/Plans";
import Subscriptions from "../pages/Subscriptions";
import Devices from "../pages/Devices";
import NotFound from "../pages/NotFound";

import MainLayout from "../layouts/MainLayout";

function AppRoutes() {
    return (
        <MainLayout>
            <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/customers" element={<Customers />} />
                <Route path="/plans" element={<Plans />} />
                <Route path="/subscriptions" element={<Subscriptions />} />
                <Route path="/devices" element={<Devices />} />
                <Route path="*" element={<NotFound />} />
            </Routes>
        </MainLayout>
    );
}

export default AppRoutes;