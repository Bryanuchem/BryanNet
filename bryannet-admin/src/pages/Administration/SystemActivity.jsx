import EmptyState from "../../components/common/EmptyState";
import PageHeader from "../../components/common/PageHeader";

export default function SystemActivity() {
    return (
        <>
            <PageHeader
                title="System Activity"
                subtitle="View important events occurring across the platform."
            />

            <EmptyState
                title="No System Activity"
                description="System events will appear here as more platform features are integrated."
            />
        </>
    );
}