import EmptyState from "../../components/common/EmptyState";
import PageHeader from "../../components/common/PageHeader";

export default function AdminUsers() {
    return (
        <>
            <PageHeader
                title="Admin Users"
                subtitle="Manage dashboard administrators and their accounts."
            />

            <EmptyState
                title="No Administrator Management Yet"
                description="Administrator management features will be implemented in the next phase."
            />
        </>
    );
}