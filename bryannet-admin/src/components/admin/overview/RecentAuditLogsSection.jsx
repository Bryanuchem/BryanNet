import { Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

import SectionHeader from "../common/SectionHeader";
import RecentAuditLogsTable from "./RecentAuditLogsTable";

export default function RecentAuditLogsSection({
    logs,
    loading,
}) {
    const navigate = useNavigate();

    return (
        <>
            <SectionHeader
                title="Recent Audit Logs"
                subtitle="Latest administrative actions across the platform."
                action={
                    <Button
                        size="small"
                        onClick={() =>
                            navigate("/administration/audit-logs")
                        }
                    >
                        View All
                    </Button>
                }
            />

            <RecentAuditLogsTable
                logs={logs}
                loading={loading}
            />
        </>
    );
}