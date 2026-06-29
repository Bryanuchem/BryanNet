import EmptyState from "../../components/common/EmptyState";
import PageHeader from "../../components/common/PageHeader";

export default function LoginSessions() {
    return (
        <>
            <PageHeader
                title="Login Sessions"
                subtitle="Monitor active administrator sessions."
            />

            <EmptyState
                title="No Active Session Information"
                description="Administrator login sessions will be displayed here."
            />
        </>
    );
}