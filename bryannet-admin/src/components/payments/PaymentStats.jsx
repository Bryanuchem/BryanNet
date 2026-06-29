import {
    Grid,
} from "@mui/material";

import DashboardStatCard from "../common/DashboardStatCard";

function PaymentStats({
    summary,
    isLoading,
}) {

    return (

        <Grid
            container
            spacing={3}
            sx={{
                mb: 3,
            }}
        >

            <Grid
                size={{
                    xs: 12,
                    sm: 6,
                    lg: 3,
                }}
            >

                <DashboardStatCard
                    title="Total Revenue"
                    value={
                        summary
                            ? `₦${Number(
                                  summary.total_revenue,
                              ).toLocaleString()}`
                            : "₦0"
                    }
                    loading={isLoading}
                />

            </Grid>

            <Grid
                size={{
                    xs: 12,
                    sm: 6,
                    lg: 3,
                }}
            >

                <DashboardStatCard
                    title="Total Payments"
                    value={
                        summary?.total_payments ?? 0
                    }
                    loading={isLoading}
                />

            </Grid>

            <Grid
                size={{
                    xs: 12,
                    sm: 6,
                    lg: 3,
                }}
            >

                <DashboardStatCard
                    title="Pending Payments"
                    value={
                        summary?.pending_payments ?? 0
                    }
                    loading={isLoading}
                />

            </Grid>

            <Grid
                size={{
                    xs: 12,
                    sm: 6,
                    lg: 3,
                }}
            >

                <DashboardStatCard
                    title="Failed Payments"
                    value={
                        summary?.failed_payments ?? 0
                    }
                    loading={isLoading}
                />

            </Grid>

        </Grid>

    );

}

export default PaymentStats;