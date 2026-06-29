import EmptyState from "../../components/common/EmptyState";
import PageHeader from "../../components/common/PageHeader";

export default function RolesPermissions() {
    return (
        <>
            <PageHeader
                title="Roles & Permissions"
                subtitle="Configure administrator roles and access permissions."
            />

            <EmptyState
                title="No Roles Configured"
                description="Role and permission management will be implemented in a later step."
            />
        </>
    );
}