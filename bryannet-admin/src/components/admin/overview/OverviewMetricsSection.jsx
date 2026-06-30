import { Grid } from "@mui/material";
import {
    AdminPanelSettings,
    Badge,
    History,
    Login,
    Timeline,
} from "@mui/icons-material";

import SectionHeader from "../common/SectionHeader";
import OverviewMetricCard from "./OverviewMetricCard";

export default function OverviewMetricsSection({
    metrics,
    loading,
}) {
    return (
        <>
            <SectionHeader
                title="Overview Metrics"
                subtitle="Key administration statistics."
            />

            <Grid container spacing={3} sx={{ mb: 4 }}>
                <Grid size={{ xs: 12, sm: 6, md: 4, lg: 2.4 }}>
                    <OverviewMetricCard
                        title="Administrators"
                        value={metrics?.admin_users ?? 0}
                        subtitle="Administrator accounts"
                        icon={<AdminPanelSettings color="primary" />}
                        loading={loading}
                    />
                </Grid>

                <Grid size={{ xs: 12, sm: 6, md: 4, lg: 2.4 }}>
                    <OverviewMetricCard
                        title="Active Sessions"
                        value={metrics?.active_sessions ?? 0}
                        subtitle="Currently logged in"
                        icon={<Login color="success" />}
                        loading={loading}
                    />
                </Grid>

                <Grid size={{ xs: 12, sm: 6, md: 4, lg: 2.4 }}>
                    <OverviewMetricCard
                        title="Roles"
                        value={metrics?.roles ?? 0}
                        subtitle="Configured roles"
                        icon={<Badge color="secondary" />}
                        loading={loading}
                    />
                </Grid>

                <Grid size={{ xs: 12, sm: 6, md: 6, lg: 2.4 }}>
                    <OverviewMetricCard
                        title="Audit Events"
                        value={metrics?.audit_events_today ?? 0}
                        subtitle="Recorded today"
                        icon={<History color="warning" />}
                        loading={loading}
                    />
                </Grid>

                <Grid size={{ xs: 12, sm: 6, md: 6, lg: 2.4 }}>
                    <OverviewMetricCard
                        title="System Events"
                        value={metrics?.system_events_today ?? 0}
                        subtitle="Generated today"
                        icon={<Timeline color="info" />}
                        loading={loading}
                    />
                </Grid>
            </Grid>
        </>
    );
}