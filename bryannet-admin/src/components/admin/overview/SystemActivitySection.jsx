import { Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

import {

    useCurrentPermissions,

} from "../../../hooks/useCurrentPermissions";

import SectionHeader from "../common/SectionHeader";
import RecentSystemActivityTable from "./RecentSystemActivityTable";

export default function SystemActivitySection({
    activity,
    loading,
}) {

    const navigate = useNavigate();

    const {

        hasPermission,

    } = useCurrentPermissions();

    return hasPermission(

        "system_activity.view",

    ) ? (

        <>

            <SectionHeader

                title="Recent System Activity"

                subtitle="Last 5 system events across the platform."

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

            <RecentSystemActivityTable

                activities={activity}

                loading={loading}

            />

        </>

    ) : null;
}