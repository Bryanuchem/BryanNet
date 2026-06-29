import EmptyState from "../../components/common/EmptyState";
import PageHeader from "../../components/common/PageHeader";

export default function Overview() {
    return (
        <>
            <PageHeader
                title="Administration"
                subtitle="Manage administrators, roles, security, and system activity."
            />

            <EmptyState
                title="Administration Overview"
                description="Administration overview widgets will appear here as this module is implemented."
            />
        </>
    );
}