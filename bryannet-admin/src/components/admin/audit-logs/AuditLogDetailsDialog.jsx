import SecurityOutlinedIcon from "@mui/icons-material/SecurityOutlined";

import FormDialog from "../../common/FormDialog";
import FormSection from "../../common/FormSection";
import FormGrid from "../../common/FormGrid";
import FormGridItem from "../../common/FormGridItem";
import InfoField from "../../common/InfoField";
import BadgeChip from "../../common/BadgeChip";

function AuditLogDetailsDialog({

    open,

    auditLog,

    onClose,

}) {

    if (!auditLog) {

        return null;

    }

    return (

        <FormDialog

            open={open}

            title="Audit Log Details"

            subtitle="View complete information about this audit event."

            icon={

                <SecurityOutlinedIcon

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

                title="Event Information"

                subtitle="Details of the recorded audit event."

            >

                <FormGrid>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Action"

                        >

                            {auditLog.action}

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Result"

                        >

                            <BadgeChip

                                status={

                                    auditLog.result

                                        ?.toLowerCase()

                                }

                                label={

                                    auditLog.result

                                }

                            />

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Entity"

                        >

                            {

                                auditLog.entity_type

                            }

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Target"

                        >

                            {

                                auditLog.target_name

                                ||

                                "-"

                            }

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem>

                        <InfoField

                            label="Description"

                        >

                            {

                                auditLog.description

                            }

                        </InfoField>

                    </FormGridItem>

                </FormGrid>

            </FormSection>

            <FormSection

                title="Administrator Information"

                subtitle="Administrator responsible for this event."

            >

                <FormGrid>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Administrator ID"

                        >

                            {

                                auditLog.admin_id

                                ??

                                "-"

                            }

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Session ID"

                        >

                            {

                                auditLog.admin_session_id

                                ??

                                "-"

                            }

                        </InfoField>

                    </FormGridItem>

                </FormGrid>

            </FormSection>

            <FormSection

                title="Request Information"

                subtitle="Technical information captured during the request."

            >

                <FormGrid>

                    <FormGridItem md={6}>

                        <InfoField

                            label="IP Address"

                        >

                            {

                                auditLog.ip_address

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

                                auditLog.user_agent

                                ||

                                "-"

                            }

                        </InfoField>

                    </FormGridItem>

                </FormGrid>

            </FormSection>

            <FormSection

                title="Record Information"

                subtitle="Audit log metadata."

                divider={false}

            >

                <FormGrid>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Audit Log ID"

                        >

                            {

                                auditLog.audit_log_id

                            }

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Created"

                        >

                            {

                                auditLog.created_at

                                    ? new Date(

                                        auditLog.created_at,

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

export default AuditLogDetailsDialog;