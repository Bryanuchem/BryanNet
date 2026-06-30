import { Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

import SectionHeader from "../common/SectionHeader";
import SystemActivityTimeline from "./SystemActivityTimeline";

export default function SystemActivitySection({
    activity,
    loading,
}) {
    const navigate = useNavigate();

    return (
        <>
            <SectionHeader
                title="Today's System Activity"
                subtitle="Recent background events across the platform."
                action={
                    <Button
                        size="small"
                        onClick={() =>
                            navigate("/administration/system-activity")
                        }
                    >
                        View All
                    </Button>
                }
            />

            <SystemActivityTimeline
                activity={activity}
                loading={loading}
            />
        </>
    );
}