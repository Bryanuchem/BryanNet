import { Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

import SectionHeader from "../common/SectionHeader";
import RecentLoginSessionsTable from "./RecentLoginSessionsTable";

import {

    useCurrentPermissions,

} from "../../../hooks/useCurrentPermissions";


export default function ActiveSessionsSection({
    sessions,
    loading,
}) {
    const navigate = useNavigate();

    const {

        hasPermission,

    } = useCurrentPermissions();
    
    return hasPermission(

        "login_sessions.view",

    ) ? (

        <>

            <SectionHeader

                title="Recent Login Sessions"

                subtitle="Last 5 administrator login sessions."

                action={

                    <Button

                        size="small"

                        onClick={() =>

                            navigate("/administration/sessions")

                        }

                    >

                        View All

                    </Button>

                }

            />

            <RecentLoginSessionsTable

                sessions={sessions}

                loading={loading}

            />

        </>

    ) : null;

}