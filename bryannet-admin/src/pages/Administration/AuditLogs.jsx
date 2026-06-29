import EmptyState from "../../components/common/EmptyState";
import PageHeader from "../../components/common/PageHeader";

export default function AuditLogs() {
    return (
        <>
            <PageHeader
                title="Audit Logs"
                subtitle="Track administrator actions across the platform."
            />

            <EmptyState
                title="No Audit Logs"
                description="Audit logs will appear here once activity tracking is implemented."
            />
        </>
    );
}