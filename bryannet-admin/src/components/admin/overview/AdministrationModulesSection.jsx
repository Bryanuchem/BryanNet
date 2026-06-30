import { Grid } from "@mui/material";
import {
    AdminPanelSettings,
    Security,
    History,
    Login,
    Timeline,
} from "@mui/icons-material";
import { useNavigate } from "react-router-dom";

import SectionHeader from "../common/SectionHeader";
import AdministrationModuleCard from "./AdministrationModuleCard";

export default function AdministrationModulesSection() {
    const navigate = useNavigate();

    return (
        <>
            <SectionHeader
                title="Administration Modules"
                subtitle="Quick access to administration features."
            />

            <Grid container spacing={3} sx={{ mb: 4 }}>
                <Grid size={{ xs: 12, md: 4 }}>
                    <AdministrationModuleCard
                        title="Admin Users"
                        description="Manage administrator accounts and access."
                        icon={<AdminPanelSettings color="primary" />}
                        onClick={() => navigate("/administration/admin-users")}
                    />
                </Grid>

                <Grid size={{ xs: 12, md: 4 }}>
                    <AdministrationModuleCard
                        title="Roles & Permissions"
                        description="Configure roles and module permissions."
                        icon={<Security color="secondary" />}
                        onClick={() =>
                            navigate("/administration/roles-permissions")
                        }
                    />
                </Grid>

                <Grid size={{ xs: 12, md: 4 }}>
                    <AdministrationModuleCard
                        title="Audit Logs"
                        description="Review administrator actions and changes."
                        icon={<History color="warning" />}
                        onClick={() =>
                            navigate("/administration/audit-logs")
                        }
                    />
                </Grid>

                <Grid size={{ xs: 12, md: 6 }}>
                    <AdministrationModuleCard
                        title="Login Sessions"
                        description="Monitor active administrator sessions."
                        icon={<Login color="success" />}
                        onClick={() =>
                            navigate("/administration/login-sessions")
                        }
                    />
                </Grid>

                <Grid size={{ xs: 12, md: 6 }}>
                    <AdministrationModuleCard
                        title="System Activity"
                        description="View background system events and activity."
                        icon={<Timeline color="info" />}
                        onClick={() =>
                            navigate("/administration/system-activity")
                        }
                    />
                </Grid>
            </Grid>
        </>
    );
}