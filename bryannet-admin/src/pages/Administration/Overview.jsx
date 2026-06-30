import PageHeader from "../../components/common/PageHeader";

import OverviewMetricsSection from "../../components/admin/overview/OverviewMetricsSection";
import AdministrationModulesSection from "../../components/admin/overview/AdministrationModulesSection";
import RecentAuditLogsSection from "../../components/admin/overview/RecentAuditLogsSection";
import ActiveSessionsSection from "../../components/admin/overview/ActiveSessionsSection";
import SystemActivitySection from "../../components/admin/overview/SystemActivitySection";

import { useAdministrationOverview } from "../../hooks/useAdministrationOverview";

export default function Overview() {
    const {
        data,
        isLoading,
    } = useAdministrationOverview();

    return (
        <>
            <PageHeader
                title="Administration Overview"
                subtitle="Monitor administrator access, security, and system activity."
            />

            <OverviewMetricsSection
                metrics={data?.metrics}
                loading={isLoading}
            />

            <AdministrationModulesSection />

            <RecentAuditLogsSection
                logs={data?.recent_audit_logs}
                loading={isLoading}
            />

            <ActiveSessionsSection
                sessions={data?.active_sessions}
                loading={isLoading}
            />

            <SystemActivitySection
                activity={data?.system_activity}
                loading={isLoading}
            />
        </>
    );
}