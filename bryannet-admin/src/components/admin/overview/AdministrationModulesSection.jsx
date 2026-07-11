import { Grid } from "@mui/material";
import {
    AdminPanelSettings,
    Security,
    History,
    Login,
    Timeline,
} from "@mui/icons-material";
import { useNavigate } from "react-router-dom";

import {
    useCurrentPermissions,
} from "../../../hooks/useCurrentPermissions";

import SectionHeader from "../common/SectionHeader";
import AdministrationModuleCard from "./AdministrationModuleCard";

export default function AdministrationModulesSection() {

    const navigate = useNavigate();

    const {

        hasPermission,

    } = useCurrentPermissions();

    const canViewAdministrationModules =

        hasPermission("admin_users.view") ||

        hasPermission("roles.view") ||

        hasPermission("audit_logs.view") ||

        hasPermission("login_sessions.view") ||

        hasPermission("system_activity.view");

    if (

        !canViewAdministrationModules

    ) {

        return null;

    }

    return (

        <>

            <SectionHeader

                title="Administration Modules"

                subtitle="Quick access to administration features."

            />

            <Grid

                container

                spacing={2}

                sx={{ mb: 4 }}

            >

                {hasPermission(

                    "admin_users.view",

                ) && (

                    <Grid size={{ xs: 12, md: 2.4 }}>

                        <AdministrationModuleCard

                            title="Admin Users"

                            description="Manage administrator accounts and access."

                            icon={<AdminPanelSettings color="primary" />}

                            onClick={() =>

                                navigate("/administration/users")

                            }

                        />

                    </Grid>

                )}

                {hasPermission(

                    "roles.view",

                ) && (

                    <Grid size={{ xs: 12, md: 2.4 }}>

                        <AdministrationModuleCard

                            title="Roles & Permissions"

                            description="Configure roles and module permissions."

                            icon={<Security color="secondary" />}

                            onClick={() =>

                                navigate("/administration/roles")

                            }

                        />

                    </Grid>

                )}

                {hasPermission(

                    "audit_logs.view",

                ) && (

                    <Grid size={{ xs: 12, md: 2.4 }}>

                        <AdministrationModuleCard

                            title="Audit Logs"

                            description="Review administrator actions and changes."

                            icon={<History color="warning" />}

                            onClick={() =>

                                navigate("/administration/audit-logs")

                            }

                        />

                    </Grid>

                )}

                {hasPermission(

                    "login_sessions.view",

                ) && (

                    <Grid size={{ xs: 12, md: 2.4 }}>

                        <AdministrationModuleCard

                            title="Login Sessions"

                            description="Monitor active administrator sessions."

                            icon={<Login color="success" />}

                            onClick={() =>

                                navigate("/administration/sessions")

                            }

                        />

                    </Grid>

                )}

                {hasPermission(

                    "system_activity.view",

                ) && (

                    <Grid size={{ xs: 12, md: 2.4 }}>

                        <AdministrationModuleCard

                            title="System Activity"

                            description="View background system events and activity."

                            icon={<Timeline color="info" />}

                            onClick={() =>

                                navigate("/administration/system-activity")

                            }

                        />

                    </Grid>

                )}

            </Grid>

        </>

    );

}