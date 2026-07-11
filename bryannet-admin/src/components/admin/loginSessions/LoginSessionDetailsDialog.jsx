import ComputerOutlinedIcon from "@mui/icons-material/ComputerOutlined";

import FormDialog from "../../common/FormDialog";
import FormSection from "../../common/FormSection";
import FormGrid from "../../common/FormGrid";
import FormGridItem from "../../common/FormGridItem";
import InfoField from "../../common/InfoField";
import BadgeChip from "../../common/BadgeChip";

function LoginSessionDetailsDialog({

    open,

    session,

    onClose,

}) {

    if (!session) {

        return null;

    }

    return (

        <FormDialog

            open={open}

            title="Login Session Details"

            subtitle="View complete information about this administrator session."

            icon={

                <ComputerOutlinedIcon

                    color="primary"

                    fontSize="large"

                />

            }

            maxWidth="md"

            submitText="Close"

            onSubmit={onClose}

            onClose={onClose}

            hideCancel

        >

            <FormSection

                title="Session Information"

                subtitle="Details about the login session."

            >

                <FormGrid>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Status"

                        >

                            <BadgeChip

                                status={

                                    session.is_active

                                        ? "success"

                                        : "inactive"

                                }

                                label={

                                    session.is_active

                                        ? "Active"

                                        : "Inactive"

                                }

                            />

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Login Source"

                        >

                            {

                                session.login_source

                            }

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Client"

                        >

                            {

                                session.client_name

                            }

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Logout Reason"

                        >

                            {

                                session.logout_reason

                                ||

                                "-"

                            }

                        </InfoField>

                    </FormGridItem>

                </FormGrid>

            </FormSection>

            <FormSection

                title="Administrator Information"

                subtitle="Administrator associated with this session."

            >

                <FormGrid>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Administrator ID"

                        >

                            {

                                session.admin_user_id

                            }

                        </InfoField>

                    </FormGridItem>

                </FormGrid>

            </FormSection>

            <FormSection

                title="Request Information"

                subtitle="Connection details captured during login."

            >

                <FormGrid>

                    <FormGridItem md={6}>

                        <InfoField

                            label="IP Address"

                        >

                            {

                                session.ip_address

                                ||

                                "-"

                            }

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <InfoField

                            label="User Agent"

                        >

                            {

                                session.user_agent

                                ||

                                "-"

                            }

                        </InfoField>

                    </FormGridItem>

                </FormGrid>

            </FormSection>

            <FormSection

                title="Timeline"

                subtitle="Important timestamps for this session."

            >

                <FormGrid>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Login Time"

                        >

                            {

                                session.login_time

                                    ? new Date(

                                        session.login_time,

                                    ).toLocaleString()

                                    : "-"

                            }

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Last Activity"

                        >

                            {

                                session.last_activity

                                    ? new Date(

                                        session.last_activity,

                                    ).toLocaleString()

                                    : "-"

                            }

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Logout Time"

                        >

                            {

                                session.logout_time

                                    ? new Date(

                                        session.logout_time,

                                    ).toLocaleString()

                                    : "-"

                            }

                        </InfoField>

                    </FormGridItem>

                </FormGrid>

            </FormSection>

            <FormSection

                title="Record Information"

                subtitle="Login session metadata."

                divider={false}

            >

                <FormGrid>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Session ID"

                        >

                            {

                                session.admin_session_id

                            }

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Created"

                        >

                            {

                                session.login_time

                                    ? new Date(

                                        session.login_time,

                                    ).toLocaleString()

                                    : "-"

                            }

                        </InfoField>

                    </FormGridItem>

                </FormGrid>

            </FormSection>

        </FormDialog>

    );

}

export default LoginSessionDetailsDialog;