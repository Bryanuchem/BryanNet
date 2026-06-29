import {
    Grid,
} from "@mui/material";

import RevenueChart from "./RevenueChart";
import SubscriptionBreakdown from "./SubscriptionBreakdown";

function DashboardCharts() {

    return (

        <Grid
            container
            spacing={3}
            sx={{
                mb: 4,
            }}
        >

            <Grid
                size={{
                    xs: 12,
                    lg: 8,
                }}
            >

                <RevenueChart />

            </Grid>

            <Grid
                size={{
                    xs: 12,
                    lg: 4,
                }}
            >

                <SubscriptionBreakdown />

            </Grid>

        </Grid>

    );

}

export default DashboardCharts;