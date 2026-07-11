import { Box } from "@mui/material";

import {
    AdminPanelSettings,
    Security,
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

            <Box
                sx={{
                    display: "grid",

                    gridTemplateColumns:
                        "repeat(5, minmax(0, 1fr))",

                    gap: 3,

                    mb: 4,
                }}
            >
                <OverviewMetricCard
                    title="Administrators"
                    value={metrics?.admin_users ?? 0}
                    subtitle="Administrator accounts"
                    icon={<AdminPanelSettings color="primary" />}
                    loading={loading}
                />

                <OverviewMetricCard
                    title="Roles"
                    value={metrics?.roles ?? 0}
                    subtitle="Configured roles"
                    icon={<Security color="secondary" />}
                    loading={loading}
                />

                <OverviewMetricCard
                    title="Audit Events"
                    value={metrics?.audit_events_today ?? 0}
                    subtitle="Recorded today"
                    icon={<History color="warning" />}
                    loading={loading}
                />

                <OverviewMetricCard
                    title="Login Sessions"
                    value={metrics?.login_sessions_today ?? 0}
                    subtitle="Recorded today"
                    icon={<Login color="success" />}
                    loading={loading}
                />

                <OverviewMetricCard
                    title="System Events"
                    value={metrics?.system_events_today ?? 0}
                    subtitle="Generated today"
                    icon={<Timeline color="info" />}
                    loading={loading}
                />
            </Box>
        </>
    );
}