import {
    Box,
    Grid,
} from "@mui/material";

import PageHeader from "../../components/common/PageHeader";

import DashboardStats from "../../components/dashboard/DashboardStats";
import DashboardCharts from "../../components/dashboard/DashboardCharts";
import RecentCustomers from "../../components/dashboard/RecentCustomers";
import RecentActivity from "../../components/dashboard/RecentActivity";

import {
    DashboardFiltersProvider,
} from "../../context/DashboardFiltersContext";

function DashboardContent() {

    return (

        <Box>

            <PageHeader

                title="Dashboard"

                subtitle="Monitor your ISP operations at a glance."

            />

            <DashboardStats />

            <DashboardCharts />

            <Grid
                container
                spacing={3}
            >

                <Grid
                    size={{
                        xs: 12,
                        lg: 7,
                    }}
                >

                    <RecentCustomers />

                </Grid>

                <Grid
                    size={{
                        xs: 12,
                        lg: 5,
                    }}
                >

                    <RecentActivity />

                </Grid>

            </Grid>

        </Box>

    );

}

function Dashboard() {

    return (

        <DashboardFiltersProvider>

            <DashboardContent />

        </DashboardFiltersProvider>

    );

}

export default Dashboard;