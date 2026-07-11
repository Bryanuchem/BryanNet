import {
    Grid,
} from "@mui/material";

import {
    Devices,
    Payments,
    People,
    WarningAmber,
    Wifi,
} from "@mui/icons-material";

import StatCard from "../common/StatCard";

import useDashboardSummary from "../../hooks/useDashboardSummary";

function DashboardStats() {

    const {
        data,
        isLoading,
    } = useDashboardSummary();

    return (

        <Grid
            container
            spacing={3}
            sx={{ mb: 4 }}
        >

            <Grid size={{ xs: 12, sm: 6, md: 4, lg: 2.4 }}>

                <StatCard
                    title="Customers"
                    value={data?.total_customers ?? 0}
                    icon={<People />}
                    color="primary"
                    loading={isLoading}
                />

            </Grid>

            <Grid size={{ xs: 12, sm: 6, md: 4, lg: 2.4 }}>

                <StatCard
                    title="Active Subscriptions"
                    value={data?.active_subscriptions ?? 0}
                    icon={<Wifi />}
                    color="success"
                    loading={isLoading}
                />

            </Grid>

            <Grid size={{ xs: 12, sm: 6, md: 4, lg: 2.4 }}>

                <StatCard
                    title="Active Devices"
                    value={data?.active_devices ?? 0}
                    icon={<Devices />}
                    color="info"
                    loading={isLoading}
                />

            </Grid>

            <Grid size={{ xs: 12, sm: 6, md: 6, lg: 2.4 }}>

                <StatCard
                    title="Total Revenue"
                    value={`₦${Number(
                        data?.total_revenue ?? 0
                    ).toLocaleString()}`}
                    icon={<Payments />}
                    color="warning"
                    loading={isLoading}
                />

            </Grid>

            <Grid size={{ xs: 12, sm: 6, md: 6, lg: 2.4 }}>

                <StatCard
                    title="Expiring Today"
                    value={data?.expiring_today ?? 0}
                    icon={<WarningAmber />}
                    color="error"
                    loading={isLoading}
                />

            </Grid>

        </Grid>

    );

}

export default DashboardStats;