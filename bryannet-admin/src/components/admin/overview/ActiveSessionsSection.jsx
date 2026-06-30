import { Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

import SectionHeader from "../common/SectionHeader";
import ActiveSessionsTable from "./ActiveSessionsTable";

export default function ActiveSessionsSection({
    sessions,
    loading,
}) {
    const navigate = useNavigate();

    return (
        <>
            <SectionHeader
                title="Active Login Sessions"
                subtitle="Administrators currently signed in to the platform."
                action={
                    <Button
                        size="small"
                        onClick={() =>
                            navigate("/administration/login-sessions")
                        }
                    >
                        View All
                    </Button>
                }
            />

            <ActiveSessionsTable
                sessions={sessions}
                loading={loading}
            />
        </>
    );
}